#include "include.hpp"
#include "mycode.hpp"

using namespace std;


void Users :: init(Connector *_connector){
	bpuser.init("bpuser_file", "bpuser_disk");
}

char * Users :: print_user(user _user){
    char* an;
    char buf[256];
    snprintf(buf, 256,"%s %s %s %s %d", _user.username, _user.password,  _user.name, _user.mailaddr, _user.privilege);
	an = buf;
	return an;
}

const char* Users :: add_user(const char *c, const char *u, const char *p, const char *n, const char *m, const int g){
	pair<int, int> hash_c = Hash_table().hash(c), hash_u = Hash_table().hash(u);
	if(bpuser.exist(hash_u)){return "-1";}
	if(bpuser.empty() || !strcmp(c, "!")){
		user new_user(u, p, n, m, 10, 0);
		bpuser.insert(hash_u, new_user);
		return "0";
	}
	else{
		if(!bpuser.exist(hash_c)){return "-1";}
		user cur_user = bpuser.find(hash_c);
		if((!cur_user.islogin) || (cur_user.privilege <= g)){return "-1";}
		user new_user(u, p, n, m, g, 0);
		bpuser.insert(hash_u, new_user);
		return "0";
	}
}

const char* Users :: login(const char *u, const char *p){
	pair<int, int> hash_u= Hash_table().hash(u);
	if(!bpuser.exist(hash_u)){return "-1";}
	user cur_user = bpuser.find(hash_u);
	if(cur_user.islogin || strcmp(p, cur_user.password)){return "-1";}
	cur_user.islogin = 1;
	bpuser.change(hash_u, cur_user);
	return "0";
}

const char* Users :: logout(const char *u){
	pair<int, int> hash_u= Hash_table().hash(u);
	if(!bpuser.exist(hash_u)){return "-1";}
	user cur_user = bpuser.find(hash_u);
	if((!cur_user.islogin)){return "-1";}
	cur_user.islogin = 0;
	bpuser.change(hash_u, cur_user);
    return "0";
}

const char* Users :: query_profile(const char *c, const char *u){
	pair<int, int> hash_c = Hash_table().hash(c), hash_u = Hash_table().hash(u);
	if((!bpuser.exist(hash_c)) || (!bpuser.exist(hash_u))) {return "-1";}
	user cur_user = bpuser.find(hash_c), query_user = bpuser.find(hash_u);
	if(!cur_user.islogin){return "-1";}
	if((!strcmp(c, u)) || (cur_user.privilege > query_user.privilege)){
	    return print_user(query_user);
	}
    return "-1";
}

const char* Users :: modify_profile(const char *c, const char *u, const char *p, const char *n, const char *m, const int g){
	pair<int, int> hash_c = Hash_table().hash(c), hash_u = Hash_table().hash(u);
	if((!bpuser.exist(hash_c)) || (!bpuser.exist(hash_u))) {return "-1";}
	user cur_user = bpuser.find(hash_c), modify_user = bpuser.find(hash_u);
	if(!cur_user.islogin){return "-1";}
	if(((!strcmp(c, u)) || (cur_user.privilege > modify_user.privilege)) && (g < cur_user.privilege)){
		if(strcmp(p, "!!!")) strcpy(modify_user.password, p);
		if(strcmp(n, "")) strcpy(modify_user.name, n);
		if(strcmp(m, "")) strcpy(modify_user.mailaddr, m);
		if(g != -1) modify_user.privilege = g;
		bpuser.change(hash_u, modify_user);
		return print_user(modify_user);
	}
    return "-1";
}
