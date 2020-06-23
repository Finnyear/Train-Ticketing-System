#include "include.hpp"
#include "mycode.hpp"

#define mp make_pair

using namespace std;


void Connector :: init(){
	user_controller.init(this);
	train_controller.init(this);
	order_controller.init(this);
}

void Connector :: work() {
	
	using std::string;
	using std::cin;

	string str;
	char ans[8192];

	WSADATA wsaData;
    WSAStartup(MAKEWORD(2, 2), &wsaData);
    SOCKET servSock = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP);
    sockaddr_in sockAddr;
    memset(&sockAddr, 0, sizeof(sockAddr));
    sockAddr.sin_family = AF_INET;  //使用IPv4地址
    sockAddr.sin_addr.s_addr = inet_addr("127.0.0.1");
    sockAddr.sin_port = htons(1234);  //端口
    if (bind(servSock, (LPSOCKADDR)&sockAddr, sizeof(sockAddr)) == SOCKET_ERROR){
        printf("bind error!");
    }
    if (listen(servSock, 5) == SOCKET_ERROR){
        printf("listen error!");
        return;
    }
    sockaddr_in clntAddr;
    int nSize = sizeof(clntAddr);
    SOCKET clntSock;
    char revData[8192];
    while (1){
        clntSock = accept(servSock, (SOCKADDR*)&clntAddr, &nSize);
        if (clntSock == INVALID_SOCKET){
            printf("accept error!");
            continue;
        }
        if (strcmp(inet_ntoa(clntAddr.sin_addr), "127.0.0.1")){
            printf("server attack from outside!\n");
            continue;
        }
        int ret = recv(clntSock, revData, sizeof(revData), 0);
        str = revData;
        printf("%s\n", revData);
        if( str.substr(0, 8) == "add_user" )
			strcpy(ans, add_user(str));
		else if( str.substr(0, 5) == "login" )
            strcpy(ans, login(str));
		else if( str.substr(0, 6) == "logout" )
            strcpy(ans, logout(str));
		else if( str.substr(0, 13) == "query_profile" )
            strcpy(ans, query_profile(str));
		else if( str.substr(0, 14) == "modify_profile" )
            strcpy(ans, modify_profile(str));
		else if( str.substr(0, 9) == "add_train" )
            strcpy(ans, add_train(str));
		else if( str.substr(0, 13) == "release_train" )
            strcpy(ans, release_train(str));
		else if( str.substr(0, 11) == "query_train" )
            strcpy(ans, query_train(str));
		else if( str.substr(0, 12) == "delete_train" )
            strcpy(ans, delete_train(str));
		else if( str.substr(0, 12) == "query_ticket" )
            strcpy(ans, query_ticket(str));
		else if( str.substr(0, 14) == "query_transfer" )
            strcpy(ans, query_transfer(str));
		else if( str.substr(0, 10) == "buy_ticket" )
            strcpy(ans, buy_ticket(str));
		else if( str.substr(0, 11) == "query_order" )
            strcpy(ans, query_order(str));
		else if( str.substr(0, 13) == "refund_ticket" )
            strcpy(ans, refund_ticket(str));
		else if( str.substr(0, 5) == "clean" )
			clean();
		else if( str.substr(0, 4) == "exit" ){
			exit();
			break;
		}
		printf("%s\n", ans);
        send(clntSock, ans, strlen(ans), 0);
        closesocket(clntSock);
        memset(revData, 0, sizeof(revData));
    }
    closesocket(servSock);
    WSACleanup();
}

const char* Connector :: add_user(string str){
	string *argv = nullptr;
	int argc = split(str, ' ', argv);
	string c, u, p, n, m;
	int g;
	for(int i = 1; i < argc; i += 2 ) {
		if(argv[i] == "-c") c = argv[i + 1];
		else if(argv[i] == "-u") u = argv[i + 1];
		else if(argv[i] == "-p") p = argv[i + 1];
		else if(argv[i] == "-n") n = argv[i + 1];
		else if(argv[i] == "-m") m = argv[i + 1];
		else if(argv[i] == "-g") g = read_int(argv[i + 1]);
		else assert(0);
	}
	delete []argv;
	return user_controller.add_user(c.c_str(), u.c_str(), p.c_str(), n.c_str(), m.c_str(), g);
}

const char* Connector :: login(string str){

	string *argv = nullptr;
	int argc = split(str, ' ', argv);
	string u, p;
	for(int i = 1; i < argc; i += 2 ) {
		if(argv[i] == "-u") u = argv[i + 1];
		else if(argv[i] == "-p") p = argv[i + 1];
		else assert(0);
	}
    delete []argv;
	return user_controller.login(u.c_str(), p.c_str());
}

const char* Connector :: logout(string str){
	string *argv = nullptr;
	int argc = split(str, ' ', argv);
	string u;
	for(int i = 1; i < argc; i += 2 ) {
		if(argv[i] == "-u") u = argv[i + 1];
		else assert(0);
	}
    delete []argv;
	return user_controller.logout(u.c_str());
}

const char* Connector :: query_profile(string str){
	string *argv = nullptr;
	int argc = split(str, ' ', argv);
	string c, u;
	for(int i = 1; i < argc; i += 2 ) {
		if(argv[i] == "-c") c = argv[i + 1];
		else if(argv[i] == "-u") u = argv[i + 1];
		else assert(0);
	}
    delete []argv;
	return user_controller.query_profile(c.c_str(), u.c_str());
}

const char* Connector :: modify_profile(string str){
	string *argv = nullptr;
	int argc = split(str, ' ', argv);
	string c, u, p, n, m;
	int g = -1;
	for(int i = 1; i < argc; i += 2 ) {
		if(argv[i] == "-c") c = argv[i + 1];
		else if(argv[i] == "-u") u = argv[i + 1];
		else if(argv[i] == "-p") p = argv[i + 1];
		else if(argv[i] == "-n") n = argv[i + 1];
		else if(argv[i] == "-m") m = argv[i + 1];
		else if(argv[i] == "-g") g = read_int(argv[i + 1]);
		else assert(0);
	}
    delete []argv;
	return user_controller.modify_profile(c.c_str(), u.c_str(), p.c_str(), n.c_str(), m.c_str(), g);
}

const char* Connector :: add_train(string str){
	string *argv = nullptr;
	int argc = split(str, ' ', argv);
	string ii, s, p, t, o, d, y;
	int n, m;
	Time x;
	for(int i = 1; i < argc; i += 2 ) {
		if(argv[i] == "-i") ii = argv[i + 1];
		else if(argv[i] == "-s") s = argv[i + 1];
		else if(argv[i] == "-p") p = argv[i + 1];
		else if(argv[i] == "-t") t = argv[i + 1];
		else if(argv[i] == "-o") o = argv[i + 1];
		else if(argv[i] == "-d") d = argv[i + 1];
		else if(argv[i] == "-y") y = argv[i + 1];
		else if(argv[i] == "-n") n = read_int(argv[i + 1]);
		else if(argv[i] == "-m") m = read_int(argv[i + 1]);
		else if(argv[i] == "-x") x = read_time(argv[i + 1]);
		else assert(0);
	}

	Date begindate = read_date(d.substr(0, 5));
	Date enddate = read_date(d.substr(6, 5));

	char stations[105][35];
	int prices[105], traveltimes[105], stopovertimes[105];

	string *tmp = nullptr;
	int cnt;

	cnt = split(s, '|', tmp);
	for(int i = 0; i < cnt; i++)
		strcpy(stations[i], tmp[i].c_str());
	delete []tmp;

	cnt = split(p, '|', tmp);
	for(int i = 0; i < cnt; i++)
		prices[i] = read_int(tmp[i]);
	delete []tmp;

	cnt = split(t, '|', tmp);
	for(int i = 0; i < cnt; i++)
		traveltimes[i] = read_int(tmp[i]);
	delete []tmp;

	if(n > 2){
		cnt = split(o, '|', tmp);
		for(int i = 0; i < cnt; i++)
			stopovertimes[i] = read_int(tmp[i]);
		delete []tmp;
	}
    delete []argv;
	return train_controller.add_train(ii.c_str(), n, m, stations, prices, x,
							   traveltimes, stopovertimes, begindate, enddate, y.c_str()[0]);
}

const char* Connector :: release_train(string str){
	string *argv = nullptr;
	int argc = split(str, ' ', argv);
	string ii;
	for(int i = 1; i < argc; i += 2 ) {
		if(argv[i] == "-i") ii = argv[i + 1];
		else assert(0);
	}
    delete []argv;
	return train_controller.release_train(ii.c_str());
}

const char* Connector :: query_train(string str){
	string *argv = nullptr;
	int argc = split(str, ' ', argv);
	string ii;
	Date d;
	for(int i = 1; i < argc; i += 2 ) {
		if(argv[i] == "-i") ii = argv[i + 1];
		else if(argv[i] == "-d") d = read_date(argv[i + 1]);
		else assert(0);
	}
    delete []argv;
	return train_controller.query_train(ii.c_str(), d);
}

const char* Connector :: delete_train(string str){
	string *argv = nullptr;
	int argc = split(str, ' ', argv);
	string ii;
	for(int i = 1; i < argc; i += 2 ) {
		if(argv[i] == "-i") ii = argv[i + 1];
		else assert(0);
	}
    delete []argv;
	return train_controller.delete_train(ii.c_str());
}

const char* Connector :: query_ticket(string str){
	string *argv = nullptr;
	int argc = split(str, ' ', argv);
	string s, t, p = "time";
	Date d;
	for(int i = 1; i < argc; i += 2 ) {
		if(argv[i] == "-s") s = argv[i + 1];
		else if(argv[i] == "-t") t = argv[i + 1];
		else if(argv[i] == "-p") p = argv[i + 1];
		else if(argv[i] == "-d") d = read_date(argv[i + 1]);
		else assert(0);
	}
    delete []argv;
	return train_controller.query_ticket(s.c_str(), t.c_str(), d, p.c_str());
}

const char* Connector :: query_transfer(string str){
	string *argv = nullptr;
	int argc = split(str, ' ', argv);
	string s, t, p = "time";
	Date d;
	for(int i = 1; i < argc; i += 2 ) {
		if(argv[i] == "-s") s = argv[i + 1];
		else if(argv[i] == "-t") t = argv[i + 1];
		else if(argv[i] == "-p") p = argv[i + 1];
		else if(argv[i] == "-d") d = read_date(argv[i + 1]);
		else assert(0);
	}
    delete []argv;
	return train_controller.query_transfer(s.c_str(), t.c_str(), d, p.c_str());
}

const char* Connector :: buy_ticket(string str){
	string *argv = nullptr;
	int argc = split(str, ' ', argv);
	string u, ii, f, t, q = "false";
	Date d;
	int n;
	for(int i = 1; i < argc; i += 2 ) {
		if(argv[i] == "-u") u = argv[i + 1];
		else if(argv[i] == "-i") ii = argv[i + 1];
		else if(argv[i] == "-f") f = argv[i + 1];
		else if(argv[i] == "-t") t = argv[i + 1];
		else if(argv[i] == "-q") q = argv[i + 1];
		else if(argv[i] == "-d") d = read_date(argv[i + 1]);
		else if(argv[i] == "-n") n = read_int(argv[i + 1]);
		else assert(0);
	}
    delete []argv;
	return order_controller.buy_ticket(u.c_str(), ii.c_str(), d, n, f.c_str(), t.c_str(), q.c_str());
}

const char* Connector :: query_order(string str){
	string *argv = nullptr;
	int argc = split(str, ' ', argv);
	string u;
	for(int i = 1; i < argc; i += 2 ) {
		if(argv[i] == "-u") u = argv[i + 1];
		else assert(0);
	}
    delete []argv;
	return order_controller.query_order(u.c_str());
}

const char* Connector :: refund_ticket(string str){
	string *argv = nullptr;
	int argc = split(str, ' ', argv);
	string u;
	int n = 1;
	for(int i = 1; i < argc; i += 2 ) {
		if(argv[i] == "-u") u = argv[i + 1];
		else if(argv[i] == "-n") n = read_int(argv[i + 1]);
		else assert(0);
	}
    delete []argv;
	return order_controller.refund_ticket(u.c_str(), n);
}

void Connector :: clean(){
	user_controller.bpuser.clear();
	train_controller.bpseat.clear();
	train_controller.bpstation.clear();
	train_controller.bpstrain.clear();
	train_controller.bptrain.clear();
	order_controller.bpuorder.clear();
	order_controller.bptorder.clear();
}

void Connector :: exit(){
	vector<pair<pair<int, int>, user> > user_list;
	user_list.clear();
	user_controller.bpuser.getall(user_list);
	int sz = user_list.size();
	for(int i = 0; i < sz; i++){
		user this_user = user_list[i].second;
		if(this_user.islogin){
			this_user.islogin = 0;
			user_controller.bpuser.change(user_list[i].first, this_user);
		}
	}
}

int Connector :: split(string str, char c, string *&ans){
	if(c == ' '){
		int cnt = 0;
		stringstream ss(str);
		string tmp;
		while(ss >> tmp) cnt++;
		ans = new string [cnt];
		ss = stringstream(str);
		for(int i = 0; i < cnt; i++)
			ss >> ans[i];
		return cnt;
	}
	else{
		int cnt = 1;
		for(int i = 0; i < (int)str.length(); i++)
			if(str[i] == c)
				++cnt;
		ans = new std::string[cnt];
		int now = 0;
		for(int i = 0; i < (int)str.length(); i++) {
			if(str[i] == c) ++now;
			else ans[now].push_back( str[i] );
		}
		return cnt;
	}
}

int Connector :: read_int(string str){
	int x = 0;
	for(int i = 0; i < (int)str.length(); i++)
		x = x * 10 + str[i] - '0';
	return x;
}

Time Connector :: read_time(string str){
	int hr = (str[0] - '0') * 10 + str[1] - '0';
	int mi = (str[3] - '0') * 10 + str[4] - '0';
	return Time(Date(), hr, mi);
}

Date Connector :: read_date(string str){
	int mo = (str[0] - '0') * 10 + str[1] - '0';
	int da = (str[3] - '0') * 10 + str[4] - '0';
	return Date(mo, da);
}
