#include "include.hpp"
#include "Users.hpp"
#include "Trains.hpp"
#include "Orders.hpp"

#ifndef _Connector
#define _Connector

using namespace std;

class Connector{
public:
	Users user_controller;
	Trains train_controller;
	Orders order_controller;

	void init();
	void work();
	const char * add_user(string str);
	const char * login(string str);
	const char * logout(string str);
	const char * query_profile(string str);
	const char * modify_profile(string str);
	const char * add_train(string str);
	const char * release_train(string str);
	const char * query_train(string str);
	const char * delete_train(string str);
	const char * query_ticket(string str);
	const char * query_transfer(string str);
	const char * buy_ticket(string str);
	const char * query_order(string str);
	const char * refund_ticket(string str);
	void clean();
	void exit();
	int split(string str, char c, string *&ans);
	int read_int(string str);
	Time read_time(string str);
	Date read_date(string str);
};

#endif