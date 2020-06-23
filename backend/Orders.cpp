#include "include.hpp"
#include "mycode.hpp"

#define mp make_pair

using namespace std;

void Orders :: init(Connector *_connector){
	connector = _connector;
	bpuorder.init("bpuorder_file", "bpuorder_disk");
	bptorder.init("bptorder_file", "bptorder_disk");
}

const char* Orders :: buy_ticket(const char *u, const char *i, Date d, int n, const char *f, const char *t, const char *q){
	pair<int, int> hash_u = Hash.hash(u), hash_i = Hash.hash(i), hash_f = Hash.hash(f), hash_t = Hash.hash(t);
	if(!(connector -> user_controller.bpuser.exist(hash_u))){return "-1";}
	if(!(connector -> train_controller.bptrain.exist(hash_i))){return "-1";}
	if(!(connector -> train_controller.bpstation.exist(hash_f))){return "-1";}
	if(!(connector -> train_controller.bpstation.exist(hash_t))){return "-1";}
	if(strcmp(q, "false") && strcmp(q, "true")){return "-1";}
	user this_user = connector -> user_controller.bpuser.find(hash_u);
	if(!this_user.islogin){return "-1";}
	train this_train = connector -> train_controller.bptrain.find(hash_i);
	if(!this_train.isreleased){return "-1";}
	if(n > this_train.seatnum){return "-1";}
	Station be = connector -> train_controller.bpstation.find(hash_f);
	Station en = connector -> train_controller.bpstation.find(hash_t);
	int be_cnt = be.traincnt, en_cnt = en.traincnt;
	int be_pos = -1, en_pos = -1;
	for(int i = 1; i <= be.traincnt; i++)
		if(hash_i == connector -> train_controller.bpstrain.find(mp(hash_f, i)).first){
			be_pos = connector -> train_controller.bpstrain.find(mp(hash_f, i)).second;
			break;
		}
	for(int i = 1; i <= en.traincnt; i++)
		if(hash_i == connector -> train_controller.bpstrain.find(mp(hash_t, i)).first){
			en_pos = connector -> train_controller.bpstrain.find(mp(hash_t, i)).second;
			break;
		}
	if((be_pos == -1) || (en_pos == -1) || (en_pos <= be_pos)){return "-1";}
	Time tim_be = this_train.starttime; tim_be.date = d;
	tim_be = tim_be + (this_train.traveltimes[be_pos] + this_train.stopovertimes[be_pos]);
	int dd = (d - (tim_be.date - d)) - this_train.begindate;
	if(((d - (tim_be.date - d)) < this_train.begindate) || (this_train.enddate < (d - (tim_be.date - d))))
		{return "-1";}
	tim_be.date = d;
	Time tim_en = tim_be + (this_train.traveltimes[en_pos] - 
					(this_train.traveltimes[be_pos] + this_train.stopovertimes[be_pos]));
	Ticket ticket = Ticket(i, f, t, tim_be, tim_en, this_train.prices[en_pos] - this_train.prices[be_pos], n);
	char status[25];
	Seat seat = connector -> train_controller.bpseat.find(hash_i);
	int mn = 0x7fffffff;
	for(int i = be_pos; i < en_pos; i++){
		mn = min(mn, seat.seat[dd][i]);
	}
	if(mn >= n){
		for(int i = be_pos; i < en_pos; i++)
			seat.seat[dd][i] -= n;
		strcpy(status, "success");
		connector -> train_controller.bpseat.change(hash_i, seat);
	}
	else{
		if(!strcmp(q, "true")) strcpy(status, "pending");
		else {return "-1";}
	}
	this_user.ordercnt++;
	connector -> user_controller.bpuser.change(hash_u, this_user);
	if(!strcmp(status, "pending")){
		seat.ordercnt[dd]++;
		connector -> train_controller.bpseat.change(hash_i, seat);
		connector -> train_controller.bptrain.change(hash_i, this_train);
		Order order = Order(status, u, this_user.ordercnt, i, dd, seat.ordercnt[dd], ticket);
		bptorder.insert(mp(mp(hash_i, dd), seat.ordercnt[dd]), order);
		bpuorder.insert(mp(hash_u, this_user.ordercnt), order);
        return "queue";
	}
	else{
		Order order = Order(status, u, this_user.ordercnt, i, dd, 0, ticket);
		bpuorder.insert(mp(hash_u, this_user.ordercnt), order);
        char* an;
        char buf[256];
        snprintf(buf, 256,"%d", ticket.price * ticket.seat);
        an = buf;
        return an;
	}
}

const char* Orders :: query_order(const char *u){
	pair<int, int> hash_u = Hash.hash(u);
	if(!(connector -> user_controller.bpuser.exist(hash_u))){return "-1";}
	user this_user = connector -> user_controller.bpuser.find(hash_u);
	if(!this_user.islogin){return "-1";}
    char* an;
    char buf[8192];
    snprintf(buf, sizeof(buf),"%d\n", this_user.ordercnt);
	for(int i = this_user.ordercnt; i >= 1; i--){
		Order order = bpuorder.find(mp(hash_u, i));
        char tmp[128];
		snprintf(tmp, sizeof(tmp), "[%s] %s %s %02d-%02d %02d:%02d -> %s %02d-%02d %02d:%02d %d %d\n", order.status, order.ticket.train,
				order.ticket.station_s, order.ticket.departtime.date.month, order.ticket.departtime.date.day, 
				order.ticket.departtime.hour, order.ticket.departtime.minute,
				order.ticket.station_t, order.ticket.arrivetime.date.month, order.ticket.arrivetime.date.day, 
				order.ticket.arrivetime.hour, order.ticket.arrivetime.minute, order.ticket.price, order.ticket.seat);
	    strcat(buf, tmp);
	}
    an = buf;
    return an;
}

const char* Orders :: refund_ticket(const char *u, int n){
	pair<int, int> hash_u = Hash.hash(u);
	if(!(connector -> user_controller.bpuser.exist(hash_u))){return "-1";}
	user this_user = connector -> user_controller.bpuser.find(hash_u);
	if(!this_user.islogin){return "-1";}
	if(this_user.ordercnt < n){return "-1";}
	Order order = bpuorder.find(mp(hash_u, this_user.ordercnt - n + 1));
	pair<int, int> hash_i = Hash.hash(order.trainid);
	train this_train = connector -> train_controller.bptrain.find(hash_i);
	if(!strcmp(order.status, "refunded")){return "-1";}
	else if(!strcmp(order.status, "pending")){
		strcpy(order.status, "refunded");
		bpuorder.change(mp(hash_u, order.iduser), order);
		bptorder.change(mp(mp(hash_u, order.dday), order.idtrain), order);
        return "0";
	}
	else{
		strcpy(order.status, "refunded");
		Seat seat = connector -> train_controller.bpseat.find(hash_i);
		Station be = connector -> train_controller.bpstation.find(Hash.hash(order.ticket.station_s));
		Station en = connector -> train_controller.bpstation.find(Hash.hash(order.ticket.station_t));
		int be_cnt = be.traincnt, en_cnt = en.traincnt;
		int be_pos = -1, en_pos = -1;
		for(int i = 1; i <= be.traincnt; i++)
			if(hash_i == connector -> train_controller.bpstrain.find(mp(Hash.hash(order.ticket.station_s), i)).first){
				be_pos = connector -> train_controller.bpstrain.find(mp(Hash.hash(order.ticket.station_s), i)).second;
				break;
			}
		for(int i = 1; i <= en.traincnt; i++)
			if(hash_i == connector -> train_controller.bpstrain.find(mp(Hash.hash(order.ticket.station_t), i)).first){
				en_pos = connector -> train_controller.bpstrain.find(mp(Hash.hash(order.ticket.station_t), i)).second;
				break;
			}
		for(int i = be_pos; i < en_pos; i++){
			seat.seat[order.dday][i] += order.ticket.seat;
		}
		bpuorder.change(mp(hash_u, order.iduser), order);
		bptorder.change(mp(mp(hash_u, order.dday), order.idtrain), order);
		for(int i = 1; i <= seat.ordercnt[order.dday]; i++){
			Order cur_order = bptorder.find(mp(mp(hash_i, order.dday), i));
			if(strcmp(cur_order.status, "pending")) continue;
			Station cur_be = connector -> train_controller.bpstation.find(Hash.hash(cur_order.ticket.station_s));
			Station cur_en = connector -> train_controller.bpstation.find(Hash.hash(cur_order.ticket.station_t));
			int cur_be_cnt = cur_be.traincnt, cur_en_cnt = cur_en.traincnt;
			int cur_be_pos = -1, cur_en_pos = -1;
			for(int i = 1; i <= cur_be.traincnt; i++)
				if(hash_i == connector -> train_controller.bpstrain.find(mp(Hash.hash(cur_order.ticket.station_s), i)).first){
					cur_be_pos = connector -> train_controller.bpstrain.find(mp(Hash.hash(cur_order.ticket.station_s), i)).second;
					break;
				}
			for(int i = 1; i <= cur_en.traincnt; i++)
				if(hash_i == connector -> train_controller.bpstrain.find(mp(Hash.hash(cur_order.ticket.station_t), i)).first){
					cur_en_pos = connector -> train_controller.bpstrain.find(mp(Hash.hash(cur_order.ticket.station_t), i)).second;
					break;
				}
			int mn = 0x7fffffff;
			for(int i = cur_be_pos; i < cur_en_pos; i++)
				mn = min(mn, seat.seat[order.dday][i]);
			if(mn >= cur_order.ticket.seat){
				strcpy(cur_order.status, "success");
				for(int i = cur_be_pos; i < cur_en_pos; i++)
					seat.seat[order.dday][i] -= cur_order.ticket.seat;
				bpuorder.change(mp(Hash.hash(cur_order.username), cur_order.iduser), cur_order);
				bptorder.change(mp(mp(Hash.hash(cur_order.trainid), cur_order.dday), cur_order.idtrain), cur_order);
			}
		}
		connector -> train_controller.bpseat.change(hash_i, seat);
        return "0";
	}
}
