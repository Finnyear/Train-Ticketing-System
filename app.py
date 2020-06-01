from flask import Flask, render_template, request, redirect, flash, url_for
from mine import *

app = Flask(__name__)

@app.route('/')
@app.route('/index.html')
def index():
	return render_template('index.html')

@app.route('/login.html')
def login():
	return render_template('login.html')

@app.route('/register.html')
def register():
	return render_template('register.html')

@app.route('/add_train.html', methods=['GET', 'POST'])
def add_train():
	train_id_v = train_type_v = station_num_v = seat_num_v = station_name_v = price_v = hour_v = minute_v = travel_time_v = stop_over_time_v = sale_month1_v = sale_month2_v = sale_date1_v = sale_date2_v = ''	
	if request.method == 'POST':
		train_id = request.form.get('train_id')
		train_type = request.form.get('train_type')
		station_num = request.form.get('station_num')
		seat_num = request.form.get('seat_num')
		station_name = request.form.get('station_name')
		price = request.form.get('price')
		hour = request.form.get('hour')
		minute = request.form.get('minute')
		travel_time = request.form.get('travel_time')
		stop_over_time = request.form.get('stop_over_time')
		sale_month1 = request.form.get('sale_month1')
		sale_month2 = request.form.get('sale_month2')
		sale_date1 = request.form.get('sale_date1')
		sale_date2 = request.form.get('sale_date2')

		train_id_ = id_check_valid(train_id)
		if train_id_ == '!':
			flash('Invalid input: "'+ train_id +'". (A valid train ID should be a string with an initial letter and made up of letter(s), number(s) or underline(s).)')
			return render_template('add_train.html', train_id_v=train_id, train_type_v=train_type, station_num_v=station_num, seat_num_v=seat_num, station_name_v=station_name, price_v=price, hour_v=hour, minute_v=minute, travel_time_v=travel_time, stop_over_time_v=stop_over_time, sale_month1_v=sale_month1, sale_month2_v= sale_month2, sale_date1_v=sale_date1, sale_date2_v=sale_date2)
		if len(train_type) != 1 or train_type > 'Z' or train_type < 'A':
			flash('Invalid input: "'+ train_type +'". (A valid train type should be a capital letter.)')
			return render_template('add_train.html', train_id_v=train_id, train_type_v=train_type, station_num_v=station_num, seat_num_v=seat_num, station_name_v=station_name, price_v=price, hour_v=hour, minute_v=minute, travel_time_v=travel_time, stop_over_time_v=stop_over_time, sale_month1_v=sale_month1, sale_month2_v= sale_month2, sale_date1_v=sale_date1, sale_date2_v=sale_date2)
		if not check_station_name(station_name, int(station_num)):
			flash('Invalid input: station_name.')
			return render_template('add_train.html', train_id_v=train_id, train_type_v=train_type, station_num_v=station_num, seat_num_v=seat_num, station_name_v=station_name, price_v=price, hour_v=hour, minute_v=minute, travel_time_v=travel_time, stop_over_time_v=stop_over_time, sale_month1_v=sale_month1, sale_month2_v= sale_month2, sale_date1_v=sale_date1, sale_date2_v=sale_date2)
		if not check_num(price, int(station_num) - 1, 100000):
			flash('Invalid input: price.')
			return render_template('add_train.html', train_id_v=train_id, train_type_v=train_type, station_num_v=station_num, seat_num_v=seat_num, station_name_v=station_name, price_v=price, hour_v=hour, minute_v=minute, travel_time_v=travel_time, stop_over_time_v=stop_over_time, sale_month1_v=sale_month1, sale_month2_v= sale_month2, sale_date1_v=sale_date1, sale_date2_v=sale_date2)
		if not check_num(travel_time, int(station_num) - 1, 10000):
			flash('Invalid input: travel time.')
			return render_template('add_train.html', train_id_v=train_id, train_type_v=train_type, station_num_v=station_num, seat_num_v=seat_num, station_name_v=station_name, price_v=price, hour_v=hour, minute_v=minute, travel_time_v=travel_time, stop_over_time_v=stop_over_time, sale_month1_v=sale_month1, sale_month2_v= sale_month2, sale_date1_v=sale_date1, sale_date2_v=sale_date2)
		if not check_num(stop_over_time, int(station_num) - 2, 10000):
			flash('Invalid input: stop over time.')
			return render_template('add_train.html', train_id_v=train_id, train_type_v=train_type, station_num_v=station_num, seat_num_v=seat_num, station_name_v=station_name, price_v=price, hour_v=hour, minute_v=minute, travel_time_v=travel_time, stop_over_time_v=stop_over_time, sale_month1_v=sale_month1, sale_month2_v= sale_month2, sale_date1_v=sale_date1, sale_date2_v=sale_date2)
		if not check_date(int(sale_month1), int(sale_date1)):
			flash('Invalid input: '+sale_month1+'-'+sale_date1+'.')
			return render_template('add_train.html', train_id_v=train_id, train_type_v=train_type, station_num_v=station_num, seat_num_v=seat_num, station_name_v=station_name, price_v=price, hour_v=hour, minute_v=minute, travel_time_v=travel_time, stop_over_time_v=stop_over_time, sale_month1_v=sale_month1, sale_month2_v= sale_month2, sale_date1_v=sale_date1, sale_date2_v=sale_date2)
		if (not check_date(int(sale_month2), int(sale_date2))) or (int(sale_month1) > int(sale_month2)) or ((int(sale_month1)==int(sale_month2))and(int(sale_date1)>int(sale_date2))):
			flash('Invalid input: '+sale_month2+'-'+sale_date2+'.')
			return render_template('add_train.html', train_id_v=train_id, train_type_v=train_type, station_num_v=station_num, seat_num_v=seat_num, station_name_v=station_name, price_v=price, hour_v=hour, minute_v=minute, travel_time_v=travel_time, stop_over_time_v=stop_over_time, sale_month1_v=sale_month1, sale_month2_v= sale_month2, sale_date1_v=sale_date1, sale_date2_v=sale_date2)
		
		#将train_id_送到后台并接受返回信息
		if train_id_ == 'cht':
			add_train_str = '0'
		else:
			add_train_str = '-1'
		###############################	
		if add_train_str == '-1':
			flash('Fail. Please check whether your input has obeyed the rules given below.')
			return render_template('add_train.html', train_id_v=train_id, train_type_v=train_type, station_num_v=station_num, seat_num_v=seat_num, station_name_v=station_name, price_v=price, hour_v=hour, minute_v=minute, travel_time_v=travel_time, stop_over_time_v=stop_over_time, sale_month1_v=sale_month1, sale_month2_v= sale_month2, sale_date1_v=sale_date1, sale_date2_v=sale_date2)

		flash('Success. Train: "' + train_id_ +'" has been added.')
		return redirect(url_for('add_train'))
	return render_template('add_train.html', train_id_v=train_id_v, train_type_v=train_type_v, station_num_v=station_num_v, seat_num_v=seat_num_v, station_name_v=station_name_v, price_v=price_v, hour_v=hour_v, minute_v=minute_v, travel_time_v=travel_time_v, stop_over_time_v=stop_over_time_v, sale_month1_v=sale_month1_v, sale_month2_v= sale_month2_v, sale_date1_v=sale_date1_v, sale_date2_v=sale_date2_v)

@app.route('/query_train.html', methods=['GET', 'POST'])
def query_train():
	trains = []
	train_type = ''
	train_id_ = ''
	train_id_v = ''
	month_v = ''
	date_v = ''
	q_train_display = 'display:none'
	if request.method == 'POST':
		train_id = request.form.get('train_id')
		month = request.form.get('month')
		date = request.form.get('date')
		train_id_ = id_check_valid(train_id)
		if train_id_ == '!':
			flash('Invalid input: "'+ train_id +'". (A valid train ID should be a string with an initial letter and made up of letter(s), number(s) or underline(s).)')
			return render_template('query_train.html', trains=trains, train_id=train_id_, train_type=train_type, q_train_display=q_train_display, train_id_v = train_id, month_v = month, date_v = date)
		if not check_date(month, date):
			flash('Invalid input: '+month+'-'+date+'.')
			return render_template('query_train.html', trains=trains, train_id=train_id_, train_type=train_type, q_train_display=q_train_display, train_id_v = train_id, month_v = month, date_v = date)
		#将train_id_和date送到后台并接受返回信息
		if train_id_ == 'cht':
			trains_str = "上海|xx-xx|xx:xx|12-21 |13:23| 100|50\n南京|12-22| 14:23|12-21 |17:53|100|50\n北京|12-25 |1:41|xx-xx|xx:xx |100|x"
		else:
			trains_str = '-1'
		###############################	
		if trains_str == '-1':
			flash('Train "'+ train_id +'" on '+month+'-' +date +' not found.')
			return render_template('query_train.html', trains=trains, train_id=train_id_, train_type=train_type, q_train_display=q_train_display, train_id_v = train_id, month_v = month, date_v = date)
		q_train_display = 'display:block'
		train_type = 'G'
		trains_str_ = trains_str.split('\n')
		for train_str in trains_str_:
			train_ = Train_()
			[train_.station, train_.to_date, train_.to_time, train_.from_date, train_.from_time, train_.price, train_.remain] = train_str.split('|')
			if trains_str_.index(train_str) == 0:
				train_.to_time = '-'
				train_.to_date = '-'
			if trains_str_.index(train_str) == len(trains_str_) - 1:
				train_.from_time = '-'
				train_.from_date = '-'
				train_.remain = '-'
			trains.append(train_)
	return render_template('query_train.html', trains=trains, train_id=train_id_, train_type=train_type, q_train_display=q_train_display, train_id_v = train_id_v, month_v = month_v, date_v = date_v)

@app.route('/release.html', methods=['GET', 'POST'])
def release():
	train_id_value = ''
	if request.method == 'POST':
		train_id = request.form.get('train_id')
		train_id_ = id_check_valid(train_id)
		if train_id_ == '!':
			flash('Invalid input: "'+ train_id +'". (A valid train ID should be a string with an initial letter and made up of letter(s), number(s) or underline(s).)')
			return render_template('release.html', train_id_v=train_id)
		#将train_id_送到后台并接受返回信息
		if train_id_ == 'cht':
			train_id_str = '0'
		else:
			train_id_str = '-1'
		###############################	
		if train_id_str == '-1':
			flash('Fail. Maybe go to check the train info first.')
			return render_template('release.html', train_id_v=train_id)

		flash('Success. Train: "' + train_id_ +'" has been released.')
		return redirect(url_for('release'))

	return render_template('release.html', train_id_v=train_id_value)

@app.route('/delete.html', methods=['GET', 'POST'])
def delete():
	train_id = ''
	if request.method == 'POST':
		train_id = request.form.get('train_id')
		train_id_ = id_check_valid(train_id)
		if train_id_ == '!':
			flash('Invalid input: "'+ train_id +'". (A valid train ID should be a string with an initial letter and made up of letter(s), number(s) or underline(s).)')
			return render_template('delete.html', train_id_value=train_id)
		#将train_id_送到后台并接受返回信息
		if train_id_ == 'cht':
			train_id_str = '0'
		else:
			train_id_str = '-1'
		###############################	
		if train_id_str == '-1':
			flash('Fail. Maybe go to check the train info first.')
			return render_template('delete.html', train_id_value=train_id)

		flash('Success. Train: "' + train_id_ +'" has been deleted.')
		return redirect(url_for('delete'))

	return render_template('delete.html', train_id_value=train_id)

@app.route('/add user.html', methods=['GET', 'POST'])
def add_user():
	username=password=name=email=priviledge=''
	if request.method == 'POST':
		username = request.form.get('username')
		name = request.form.get('name')
		password = request.form.get('password')
		email = request.form.get('email')
		priviledge = request.form.get('priviledge')
		username_ = id_check_valid(username)
		password_ = password_check_valid(password)
		name_ = name_check_valid(name)
		if username_ == '!':
			flash('Invalid input: "'+ username +'". (A valid username should be a string within 20 letters, with an initial letter and made up of letter(s), number(s) or underline(s).)')
			return render_template('add user.html', username_v=username, password_v=password, name_v=name, email_v=email, priviledge_v=priviledge)
		if password_ == '!':
			flash('Invalid password. (A valid password should be a string with at least 6 letters, at most 30 letters, with an initial letter and made up of letter(s), number(s) or underline(s).)')
			return render_template('add user.html', username_v=username, password_v=password, name_v=name, email_v=email, priviledge_v=priviledge)
		if name_ == '!':
			flash('Invalid name. 姓名由二至五个汉字组成。')
			return render_template('add user.html', username_v=username, password_v=password, name_v=name, email_v=email, priviledge_v=priviledge)
		#将train_id_送到后台并接受返回信息
		if username_ == 'cht':
			username_str = '0'
		else:
			username_str = '-1'
		###############################	
		if username_str == '-1':
			flash('Fail. Please check whether your input is valid.')
			return render_template('add user.html', username_v=username, password_v=password, name_v=name, email_v=email, priviledge_v=priviledge)

		flash('Success. User: "' + username_ +'" has been added.')
		return redirect(url_for('add_user'))
	return render_template('add user.html', username_v=username, password_v=password, name_v=name, email_v=email, priviledge_v=priviledge)

@app.route('/query_user.html', methods=['GET', 'POST'])
def query_user():
	user_ = User_()
	q_user_display = 'display:none'
	q_user_value = ''
	if 'name' in request.form:
		username = request.form.get('username')
		name = request.form.get('name')
		email = request.form.get('email')
		priviledge = request.form.get('priviledge')
		name_ = name_check_valid(name)
		if name_ == '!':
			flash('Invalid name. 姓名由二至五个汉字组成。')
			return render_template('query_user.html', user_=user_, q_user_display=q_user_display, q_user_value='')
		#将train_id_送到后台并接受返回信息
		if name == '爷':
			name_str = '0'
		else:
			name_str = '-1'
		###############################	
		if name_str == '-1':
			flash('Fail. Please check whether your input is valid.')
			return render_template('query_user.html', user_=user_, q_user_display=q_user_display, q_user_value='')

		flash('Success. User: "' + username +'" has been modified.')
		return redirect(url_for('query_user'))
	if request.method == 'POST':
		username = request.form.get('username')
		username_ = id_check_valid(username)
		if username_ == '!':
			flash('Invalid input: "'+ username +'". (A valid username should be a string with an initial letter and made up of letter(s), number(s) or underline(s).)')
			return render_template('query_user.html', user_=user_, q_user_display=q_user_display, q_user_value=username)
		#将train_id_送到后台并接受返回信息
		if username_ == 'cht':
			user_str = 'CHT|爷爷|cht@163.com|5'
		else:
			user_str = '-1'
		###############################	
		if user_str == '-1':
			flash('Fail. User not found.')
			return render_template('query_user.html', user_=user_, q_user_display=q_user_display, q_user_value=username)
		q_user_display = 'display:block'
		[user_.u_name, user_.name, user_.mail, user_.p_] = user_str.split('|')
	return render_template('query_user.html', user_=user_, q_user_display=q_user_display, q_user_value='')

@app.route('/query_tickets.html')
def query_tickets():
	tickets_str = 'CHT|Shanghai|12-21 |13:23|12-21 |13:23|Beijing|100|30\nCHT|Shanghai|12-21 |13:23|12-21 |13:23|Beijing|100|50'
	tickets = []
	cnt_ticket = 1
	for ticket_str in tickets_str.split('\n'):
		ticket_ = Ticket_()
		[ticket_.id_, ticket_.from_, ticket_.from_date, ticket_.from_time, ticket_.to, ticket_.to_date, ticket_.to_time, ticket_.price, ticket_.seats] = ticket_str.split('|')
		tickets.append(ticket_)
	return render_template('query_tickets.html', tickets=tickets)

@app.route('/query_order.html')
def query_order():
	orders_str = 'IS PENDING|CHT|Shanghai|12-21 |13:23|12-21 |13:23|Beijing|100|50\nIS PENDING|CHT|Shanghai|12-21 |13:23|12-21 |13:23|Beijing|100|50'
	orders = []
	for order_str in orders_str.split('\n'):
		bought_ticket = Order_()
		[bought_ticket.status, bought_ticket.id_, bought_ticket.from_, bought_ticket.from_date, bought_ticket.from_time, bought_ticket.to, bought_ticket.to_date, bought_ticket.to_time, bought_ticket.price, bought_ticket.num] = order_str.split('|')
		orders.append(bought_ticket)
	return render_template('query_order.html', orders=orders)

@app.route('/buy.html')
def buy():
	return render_template('buy.html')

@app.route('/refund.html')
def refund():
	return render_template('refund.html')

@app.route('/clear.html', methods=['GET', 'POST'])
def clear():
	if request.method == 'POST':
		#清空数据库
		return redirect(url_for('register'))
	return render_template('clear.html')

app.secret_key = 'no secret'