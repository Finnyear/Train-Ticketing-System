from flask import Flask, session, render_template, request, redirect, flash, url_for
import random as rd
from mine import *

user_num = 5
total_sale = 230
train_num = 1
released_num = 1
trains_pic = ['https://www.asqql.com/upfile/simg/2019-6/201962716363293181.jpg','https://tuchong.pstatp.com/296373/f/3950118.jpg','/static/train1.gif','/static/train2.gif','/static/train3.gif']

app = Flask(__name__)
app.config['SECRET_KEY'] = 'no secret'

@app.route('/')
@app.route('/index.html')
def index():
	if not 'C_USER' in session:
		return redirect(url_for('tourist'))
	global user_num, train_num, total_sale, released_num
	return render_template('index.html',url_=trains_pic[rd.randint(0, 4)],  C_USER=session['C_USER'], P=session['P'], total_sale = total_sale, train_num=train_num, user_num=user_num, released_num=released_num)

@app.route('/tourist.html',methods=['GET', 'POST'])
def tourist():
	if request.method == 'POST':
		return redirect(url_for('login'))
	global user_num, train_num, total_sale, released_num
	return render_template('tourist.html', url_=trains_pic[rd.randint(0, 4)], rand=rd.randint(1, 100000), total_sale = total_sale, train_num=train_num, user_num=user_num, released_num=released_num)

@app.route('/logout')
def logout():
	get_result("logout -u {}".format(session['C_USER']))
	session.pop('C_USER')
	return redirect(url_for('login'))

@app.route('/login.html',methods=['GET', 'POST'])
def login():
	u_v = ''
	if request.method == 'POST':
		user_id = request.form['id']
		password = request.form['password']
		result = get_result("login -u {} -p {}".format(user_id, password))
		if result == '0':
			session['C_USER'] = user_id
			result = get_result("query_profile -c {} -u {}".format(session['C_USER'], session['C_USER'])).split(' ')
			session['P'] = result[4]
			return redirect(url_for('index'))
		else:
			flash('Username & password not match.')
			u_v = user_id
			return render_template('login.html', u_v = u_v)
	return render_template('login.html', u_v = u_v)

@app.route('/register.html',methods=['GET', 'POST'])
def register():
	u_v=p_v=n_v=e_v=''
	if request.method == 'POST':
		password = request.form['password']
		name = request.form['name']
		email = request.form['email']
		user_id = request.form['user_id']
		user_id_ = id_check_valid(user_id)
		if user_id_ == '!':
			flash('Invalid input: '+user_id)
			return render_template('register.html', u_v=user_id, p_v = password, n_v = name, e_v = email)
		name_ = name_check_valid(name)
		if name_ == '!':
			flash('Invalid name. 姓名由二至五个汉字组成。')
			return render_template('register.html', u_v=user_id, p_v = password, n_v = name, e_v = email)
		password_ = password_check_valid(password)
		if password_ == '!':
			flash('Invalid password. (A valid password should be a string with at least 6 letters, at most 30 letters, with an initial letter and made up of letter(s), number(s) or underline(s).)')
			return render_template('register.html', u_v=user_id, p_v = password, n_v = name, e_v = email)
		result = get_result("add_user -c ! -u {} -p {} -m {} -n {}".format(user_id, password, email, name))
		if result != '-1':
			global user_num
			user_num += 1
			flash('注册成功。')
			return redirect(url_for('login'))
		else:
			flash('Fail. 用户'+ user_id +'已存在。')
			return render_template('register.html', u_v=user_id, p_v = password, n_v = name, e_v = email)
	return render_template('register.html', u_v=u_v, p_v = p_v, n_v = n_v, e_v = e_v)

@app.route('/add_train.html', methods=['GET', 'POST'])
def add_train():
	if not 'C_USER' in session:
		return redirect(url_for('login'))
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
			return render_template('add_train.html', C_USER=session['C_USER'], P=session['P'], train_id_v=train_id, train_type_v=train_type, station_num_v=station_num, seat_num_v=seat_num, station_name_v=station_name, price_v=price, hour_v=hour, minute_v=minute, travel_time_v=travel_time, stop_over_time_v=stop_over_time, sale_month1_v=sale_month1, sale_month2_v= sale_month2, sale_date1_v=sale_date1, sale_date2_v=sale_date2)
		if len(train_type) != 1 or train_type > 'Z' or train_type < 'A':
			flash('Invalid input: "'+ train_type +'". (A valid train type should be a capital letter.)')
			return render_template('add_train.html', train_id_v=train_id, train_type_v=train_type, station_num_v=station_num, seat_num_v=seat_num, station_name_v=station_name, price_v=price, hour_v=hour, minute_v=minute, travel_time_v=travel_time, stop_over_time_v=stop_over_time, sale_month1_v=sale_month1, sale_month2_v= sale_month2, sale_date1_v=sale_date1, sale_date2_v=sale_date2)
		if check_station_name(station_name, int(station_num)) == 2:
			flash('车站数量与站数不符。')
			return render_template('add_train.html', C_USER=session['C_USER'], P=session['P'], train_id_v=train_id, train_type_v=train_type, station_num_v=station_num, seat_num_v=seat_num, station_name_v=station_name, price_v=price, hour_v=hour, minute_v=minute, travel_time_v=travel_time, stop_over_time_v=stop_over_time, sale_month1_v=sale_month1, sale_month2_v= sale_month2, sale_date1_v=sale_date1, sale_date2_v=sale_date2)
		if not check_station_name(station_name, int(station_num)):
			flash('Invalid input: station_name.')
			return render_template('add_train.html', C_USER=session['C_USER'], P=session['P'], train_id_v=train_id, train_type_v=train_type, station_num_v=station_num, seat_num_v=seat_num, station_name_v=station_name, price_v=price, hour_v=hour, minute_v=minute, travel_time_v=travel_time, stop_over_time_v=stop_over_time, sale_month1_v=sale_month1, sale_month2_v= sale_month2, sale_date1_v=sale_date1, sale_date2_v=sale_date2)
		if check_num(price, int(station_num) - 1, 100000) == 2:
			flash('价格输入数量与站数不符。')
			return render_template('add_train.html', C_USER=session['C_USER'], P=session['P'], train_id_v=train_id, train_type_v=train_type, station_num_v=station_num, seat_num_v=seat_num, station_name_v=station_name, price_v=price, hour_v=hour, minute_v=minute, travel_time_v=travel_time, stop_over_time_v=stop_over_time, sale_month1_v=sale_month1, sale_month2_v= sale_month2, sale_date1_v=sale_date1, sale_date2_v=sale_date2)
		if not check_num(price, int(station_num) - 1, 100000):
			flash('Invalid input: price.')
			return render_template('add_train.html', C_USER=session['C_USER'], P=session['P'], train_id_v=train_id, train_type_v=train_type, station_num_v=station_num, seat_num_v=seat_num, station_name_v=station_name, price_v=price, hour_v=hour, minute_v=minute, travel_time_v=travel_time, stop_over_time_v=stop_over_time, sale_month1_v=sale_month1, sale_month2_v= sale_month2, sale_date1_v=sale_date1, sale_date2_v=sale_date2)
		if check_num(travel_time, int(station_num) - 1, 10000) == 2:
			flash('行车时间输入数量与站数不符。')
			return render_template('add_train.html', C_USER=session['C_USER'], P=session['P'], train_id_v=train_id, train_type_v=train_type, station_num_v=station_num, seat_num_v=seat_num, station_name_v=station_name, price_v=price, hour_v=hour, minute_v=minute, travel_time_v=travel_time, stop_over_time_v=stop_over_time, sale_month1_v=sale_month1, sale_month2_v= sale_month2, sale_date1_v=sale_date1, sale_date2_v=sale_date2)
		if not check_num(travel_time, int(station_num) - 1, 10000):
			flash('Invalid input: travel time.')
			return render_template('add_train.html', C_USER=session['C_USER'], P=session['P'], train_id_v=train_id, train_type_v=train_type, station_num_v=station_num, seat_num_v=seat_num, station_name_v=station_name, price_v=price, hour_v=hour, minute_v=minute, travel_time_v=travel_time, stop_over_time_v=stop_over_time, sale_month1_v=sale_month1, sale_month2_v= sale_month2, sale_date1_v=sale_date1, sale_date2_v=sale_date2)
		if check_num(stop_over_time, int(station_num) - 2, 10000) == 2:
			flash('经停时间输入数量与站数不符。')
			return render_template('add_train.html', C_USER=session['C_USER'], P=session['P'], train_id_v=train_id, train_type_v=train_type, station_num_v=station_num, seat_num_v=seat_num, station_name_v=station_name, price_v=price, hour_v=hour, minute_v=minute, travel_time_v=travel_time, stop_over_time_v=stop_over_time, sale_month1_v=sale_month1, sale_month2_v= sale_month2, sale_date1_v=sale_date1, sale_date2_v=sale_date2)
		if not check_num(stop_over_time, int(station_num) - 2, 10000):
			flash('Invalid input: stop over time.')
			return render_template('add_train.html', C_USER=session['C_USER'], P=session['P'], train_id_v=train_id, train_type_v=train_type, station_num_v=station_num, seat_num_v=seat_num, station_name_v=station_name, price_v=price, hour_v=hour, minute_v=minute, travel_time_v=travel_time, stop_over_time_v=stop_over_time, sale_month1_v=sale_month1, sale_month2_v= sale_month2, sale_date1_v=sale_date1, sale_date2_v=sale_date2)
		if not check_date(int(sale_month1), int(sale_date1)):
			flash('Invalid input: '+sale_month1+'-'+sale_date1+'.')
			return render_template('add_train.html', C_USER=session['C_USER'], P=session['P'], train_id_v=train_id, train_type_v=train_type, station_num_v=station_num, seat_num_v=seat_num, station_name_v=station_name, price_v=price, hour_v=hour, minute_v=minute, travel_time_v=travel_time, stop_over_time_v=stop_over_time, sale_month1_v=sale_month1, sale_month2_v= sale_month2, sale_date1_v=sale_date1, sale_date2_v=sale_date2)
		if (not check_date(int(sale_month2), int(sale_date2))) or (int(sale_month1) > int(sale_month2)) or ( (int(sale_month1)==int(sale_month2)) and (int(sale_date1)>int(sale_date2))):
			flash('Invalid input: '+sale_month2+'-'+sale_date2+'.')
			return render_template('add_train.html', C_USER=session['C_USER'], P=session['P'], train_id_v=train_id, train_type_v=train_type, station_num_v=station_num, seat_num_v=seat_num, station_name_v=station_name, price_v=price, hour_v=hour, minute_v=minute, travel_time_v=travel_time, stop_over_time_v=stop_over_time, sale_month1_v=sale_month1, sale_month2_v= sale_month2, sale_date1_v=sale_date1, sale_date2_v=sale_date2)
		date1 = form_date(sale_month1, sale_date1)
		date2 = form_date(sale_month2, sale_date2)
		start_time = form_time(hour, minute)
		add_train_str = get_result("add_train -i {} -n {} -m {} -s {} -p {} -x {} -t {} -o {} -d {}|{} -y {}".format(train_id_, station_num, seat_num, station_name, price, start_time, travel_time, stop_over_time, date1, date2, train_type))
		if add_train_str == '-1':
			flash('Fail. Please check whether your input has obeyed the rules given below.')
			return render_template('add_train.html', C_USER=session['C_USER'], P=session['P'], train_id_v=train_id, train_type_v=train_type, station_num_v=station_num, seat_num_v=seat_num, station_name_v=station_name, price_v=price, hour_v=hour, minute_v=minute, travel_time_v=travel_time, stop_over_time_v=stop_over_time, sale_month1_v=sale_month1, sale_month2_v= sale_month2, sale_date1_v=sale_date1, sale_date2_v=sale_date2)

		global train_num
		train_num += 1
		flash('Success. Train: "' + train_id_ +'" has been added.')
		return redirect(url_for('add_train'))
	return render_template('add_train.html', C_USER=session['C_USER'], P=session['P'], train_id_v=train_id_v, train_type_v=train_type_v, station_num_v=station_num_v, seat_num_v=seat_num_v, station_name_v=station_name_v, price_v=price_v, hour_v=hour_v, minute_v=minute_v, travel_time_v=travel_time_v, stop_over_time_v=stop_over_time_v, sale_month1_v=sale_month1_v, sale_month2_v= sale_month2_v, sale_date1_v=sale_date1_v, sale_date2_v=sale_date2_v)

@app.route('/query_train.html', methods=['GET', 'POST'])
def query_train():
	if not 'C_USER' in session:
		return redirect(url_for('login'))
	trains = []
	train_type = train_id_ = train_id_v = month_v = date_v = color = delete = release=disabled= ''
	q_train_display = 'display:none'
	if request.method == 'POST':
		if 'release' in request.form:
			train_id = request.form.get('train_id')
			get_result("release_train -i {}".format(train_id))
			flash("Success")
			return redirect(url_for('query_train'))
		if 'delete' in request.form:
			train_id = request.form.get('train_id')
			get_result("delete_train -i {}".format(train_id))
			flash("Success")
			return redirect(url_for('query_train'))
		train_id = request.form.get('train_id')
		month = request.form.get('month')
		date = request.form.get('date')
		train_id_ = id_check_valid(train_id)
		if train_id_ == '!':
			flash('Invalid input: "'+ train_id +'". (A valid train ID should be a string with an initial letter and made up of letter(s), number(s) or underline(s).)')
			return render_template('query_train.html', C_USER=session['C_USER'], P=session['P'], trains=trains, train_id=train_id_, train_type=train_type, q_train_display=q_train_display, train_id_v = train_id, month_v = month, date_v = date)
		if not check_date(month, date):
			flash('Invalid input: '+month+'-'+date+'.')
			return render_template('query_train.html', C_USER=session['C_USER'], P=session['P'], trains=trains, train_id=train_id_, train_type=train_type, q_train_display=q_train_display, train_id_v = train_id, month_v = month, date_v = date)
		date_ = form_date(month, date)
		trains_str = get_result("query_train -i {} -d {}".format(train_id_, date_))
		if trains_str == '-1':
			flash('Train "'+ train_id +'" on '+month+'-' +date +' not found.')
			return render_template('query_train.html', C_USER=session['C_USER'], P=session['P'], trains=trains, train_id=train_id_, train_type=train_type, q_train_display=q_train_display, train_id_v = train_id, month_v = month, date_v = date)
		q_train_display = 'display:block'
		trains_str_ = trains_str.split('\n')
		result = get_result("release_train -i !{}".format(train_id_))
		if result == "not":
			release = "Release"
		else:
			color = "grey"
			delete = "none"
			release = "Released"
			disabled = "disabled"
		for train_str in trains_str_:
			if train_str == '':
				continue
			if trains_str.index(train_str) == 0:
				train_type = train_str.split(' ')[1]
				continue
			train_ = Train_()
			[train_.station, train_.to_date, train_.to_time, train_.none_, train_.from_date, train_.from_time, train_.price, train_.remain] = train_str.split(' ')
			if trains_str_.index(train_str) == 1:
				train_.to_time = '-'
				train_.to_date = '-'
				train_.price = '-'
			if trains_str_.index(train_str) == len(trains_str_) - 1:
				train_.from_time = '-'
				train_.from_date = '-'
				train_.remain = '-'
			trains.append(train_)
	return render_template('query_train.html', C_USER=session['C_USER'], P=session['P'], trains=trains, train_id=train_id_, train_type=train_type, q_train_display=q_train_display, train_id_v = train_id_v, month_v = month_v, date_v = date_v, color = color, delete = delete, release=release, disabled=disabled)

@app.route('/release.html', methods=['GET', 'POST'])
def release():
	if not 'C_USER' in session:
		return redirect(url_for('login'))
	train_id_value = ''
	if request.method == 'POST':
		train_id = request.form.get('train_id')
		train_id_ = id_check_valid(train_id)
		if train_id_ == '!':
			flash('Invalid input: "'+ train_id +'". (A valid train ID should be a string with an initial letter and made up of letter(s), number(s) or underline(s).)')
			return render_template('release.html', C_USER=session['C_USER'], P=session['P'], train_id_v=train_id)
		train_id_str = get_result("release_train -i {}".format(train_id_))
		if train_id_str == '-1':
			flash('Fail. The train doesn\'t exit or has already been released.')
			return render_template('release.html', C_USER=session['C_USER'], P=session['P'], train_id_v=train_id)
		global released_num
		released_num+=1
		flash('Success. Train: "' + train_id_ +'" has been released.')
		return redirect(url_for('release'))

	return render_template('release.html', C_USER=session['C_USER'], P=session['P'], train_id_v=train_id_value)

@app.route('/delete.html', methods=['GET', 'POST'])
def delete():
	if not 'C_USER' in session:
		return redirect(url_for('login'))
	train_id = ''
	if request.method == 'POST':
		train_id = request.form.get('train_id')
		train_id_ = id_check_valid(train_id)
		if train_id_ == '!':
			flash('Invalid input: "'+ train_id +'". (A valid train ID should be a string with an initial letter and made up of letter(s), number(s) or underline(s).)')
			return render_template('delete.html', C_USER=session['C_USER'], P=session['P'], train_id_value=train_id)
		train_id_str = get_result("delete_train -i {}".format(train_id_))
		if train_id_str == '-1':
			flash('Fail. The train doesn\'t exit or has already been released.')
			return render_template('delete.html', C_USER=session['C_USER'], P=session['P'], train_id_value=train_id)

		global train_num
		train_num-=1
		flash('Success. Train: "' + train_id_ +'" has been deleted.')
		return redirect(url_for('delete'))

	return render_template('delete.html', C_USER=session['C_USER'], P=session['P'], train_id_value=train_id)

@app.route('/add user.html', methods=['GET', 'POST'])
def add_user():
	if not 'C_USER' in session:
		return redirect(url_for('login'))
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
			return render_template('add user.html', C_USER=session['C_USER'], P=session['P'], username_v=username, password_v=password, name_v=name, email_v=email, priviledge_v=priviledge)
		if password_ == '!':
			flash('Invalid password. (A valid password should be a string with at least 6 letters, at most 30 letters, with an initial letter and made up of letter(s), number(s) or underline(s).)')
			return render_template('add user.html', C_USER=session['C_USER'], P=session['P'], username_v=username, password_v=password, name_v=name, email_v=email, priviledge_v=priviledge)
		if name_ == '!':
			flash('Invalid name. 姓名由二至五个汉字组成。')
			return render_template('add user.html', C_USER=session['C_USER'], P=session['P'], username_v=username, password_v=password, name_v=name, email_v=email, priviledge_v=priviledge)
		username_str = get_result("add_user -c {} -u {} -p {} -n {} -m {} -g {}".format(session['C_USER'], username, password, name, email, priviledge))
		if username_str == '-1':
			flash('Fail. 用户'+ username +'已存在。')
			return render_template('add user.html', C_USER=session['C_USER'], P=session['P'], username_v=username, password_v=password, name_v=name, email_v=email, priviledge_v=priviledge)

		global user_num
		user_num+=1
		flash('Success. User: "' + username_ +'" has been added.')
		return redirect(url_for('add_user'))
	return render_template('add user.html', C_USER=session['C_USER'], P=session['P'], username_v=username, password_v=password, name_v=name, email_v=email, priviledge_v=priviledge)

@app.route('/query_user.html', methods=['GET', 'POST'])
def query_user():
	if not 'C_USER' in session:
		return redirect(url_for('login'))
	user_ = User_()
	q_user_display = 'display:none'
	q_user_value = ''
	if request.method == 'POST':
		if 'name' in request.form:
			username = request.form.get('username')
			name = request.form.get('name')
			password = request.form.get('password')
			email = request.form.get('email')
			priviledge = request.form.get('priviledge')
			password_ = password_check_valid(password)
			if password_ == '!':
				flash('Invalid password. (A valid password should be a string with at least 6 letters, at most 30 letters, with an initial letter and made up of letter(s), number(s) or underline(s).)')
				return render_template('query_user.html', C_USER=session['C_USER'], P=session['P'], user_=user_, q_user_display=q_user_display, q_user_value='')
			name_ = name_check_valid(name)
			if name_ == '!':
				flash('Invalid name. 姓名由二至五个汉字组成。')
				return render_template('query_user.html', C_USER=session['C_USER'], P=session['P'], user_=user_, q_user_display=q_user_display, q_user_value='')
			name_str = get_result("modify_profile -c {} -u {} -p {} -n {} -m {} -g {}".format(session['C_USER'], username, password, name, email, priviledge))
			if name_str == '-1':
				flash('Fail. Please check whether your input is valid.')
				return render_template('query_user.html', C_USER=session['C_USER'], P=session['P'], user_=user_, q_user_display=q_user_display, q_user_value='')

			flash('Success. User: "' + username +'" has been modified.')
			return redirect(url_for('query_user'))
		username = request.form.get('username')
		username_ = id_check_valid(username)
		if username_ == '!':
			flash('Invalid input: "'+ username +'". (A valid username should be a string with an initial letter and made up of letter(s), number(s) or underline(s).)')
			return render_template('query_user.html', C_USER=session['C_USER'], P=session['P'], user_=user_, q_user_display=q_user_display, q_user_value=username)
		user_str = get_result("query_profile -c {} -u {}".format(session['C_USER'], username))
		if user_str == '-1':
			flash('Fail. User not found.')
			return render_template('query_user.html', C_USER=session['C_USER'], P=session['P'], user_=user_, q_user_display=q_user_display, q_user_value=username)
		q_user_display = 'display:block'
		[user_.u_name, user_.password, user_.name, user_.mail, user_.p_] = user_str.split(' ')
	return render_template('query_user.html', C_USER=session['C_USER'], P=session['P'], user_=user_, q_user_display=q_user_display, q_user_value='')

@app.route('/query_tickets.html', methods=['GET','POST'])
def query_tickets():
	if not 'C_USER' in session:
		return redirect(url_for('login'))
	tickets = []
	from_v =to_v =month_v =date_v =from__v =to__v =month__v =date__v =''
	num = 2
	q_ticket_display='display:none'
	if request.method == 'POST':
		from__ = request.form.get('from')
		to = request.form.get('to')
		month = request.form.get('month')
		date = request.form.get('date')
		p_ = request.form.get('account')
		if not check_station_name(from__, 1):
			flash('Invlid input: "'+from__+'".站名应为不超过十个汉字组成。')
			return render_template('query_tickets.html', C_USER=session['C_USER'], P=session['P'], tickets=tickets, from_v=from__,to_v=to,month_v=month,date_v=date,from__v=from__v,to__v=to__v,month__v=month__v,date__v=date__v,q_ticket_display='display:none' ,num = num)
		if not check_station_name(to, 1):
			flash('Invlid input: "'+to+'".站名应为不超过十个汉字组成。')
			return render_template('query_tickets.html', C_USER=session['C_USER'], P=session['P'], tickets=tickets, from_v=from__,to_v=to,month_v=month,date_v=date,from__v=from__v,to__v=to__v,month__v=month__v,date__v=date__v,q_ticket_display='display:none' ,num = num)
		if not check_date(int(month), int(date)):
			flash('Invalid input: '+month+'-'+date+'.')
			return render_template('query_tickets.html', C_USER=session['C_USER'], P=session['P'], tickets=tickets, from_v=from__,to_v=to,month_v=month,date_v=date,from__v=from__v,to__v=to__v,month__v=month__v,date__v=date__v,q_ticket_display='display:none' ,num = num)
		date_ = form_date(month, date)
		if p_ == 'transfer one and only':
			tickets_str = get_result("query_transfer -s {} -t {} -d {}".format(from__, to, date_))
			if tickets_str == '-1':
				flash('Fail. Tickets not found.')
				return render_template('query_tickets.html', C_USER=session['C_USER'], P=session['P'], tickets=tickets, from_v=from__,to_v=to,month_v=month,date_v=date,from__v=from__v,to__v=to__v,month__v=month__v,date__v=date__v,q_ticket_display='display:none' ,num = num)
			else:
				q_ticket_display = 'display:block'
				for ticket_str in tickets_str.split('\n'):
					if ticket_str == '':
						continue
					ticket_ = Ticket_()
					[ticket_.id_, ticket_.from_, ticket_.from_date, ticket_.from_time, ticket_.none_,ticket_.to, ticket_.to_date, ticket_.to_time, ticket_.price, ticket_.seats] = ticket_str.split(' ')
					tickets.append(ticket_)
				return render_template('query_tickets.html', C_USER=session['C_USER'], P=session['P'], tickets=tickets, from_v=from_v,to_v=to_v,month_v=month_v,date_v=date_v,from__v=from__v,to__v=to__v,month__v=month__v,date__v=date__v,q_ticket_display=q_ticket_display,num = num)
		tickets_str = get_result("query_ticket -s {} -t {} -d {} -p {}".format(from__, to, date_, p_))
		if tickets_str == '-1':
			flash('Fail. Tickets not found.')
			return render_template('query_tickets.html', C_USER=session['C_USER'], P=session['P'], tickets=tickets, from_v=from__,to_v=to,month_v=month,date_v=date,from__v=from__v,to__v=to__v,month__v=month__v,date__v=date__v,q_ticket_display='display:none' ,num = num)
		else:
			q_ticket_display = 'display:block'
			for ticket_str in tickets_str.split('\n'):
				if ticket_str == '':
					continue
				if tickets_str.index(ticket_str) == 0:
					num = ticket_str
					continue
				ticket_ = Ticket_()
				[ticket_.id_, ticket_.from_, ticket_.from_date, ticket_.from_time, ticket_.none_,ticket_.to, ticket_.to_date, ticket_.to_time, ticket_.price, ticket_.seats] = ticket_str.split(' ')
				tickets.append(ticket_)

	return render_template('query_tickets.html', C_USER=session['C_USER'], P=session['P'], tickets=tickets, from_v=from_v,to_v=to_v,month_v=month_v,date_v=date_v,from__v=from__v,to__v=to__v,month__v=month__v,date__v=date__v,q_ticket_display=q_ticket_display,num = num)

@app.route('/query_order.html',methods=['GET','POST'])
def query_order():
	if not 'C_USER' in session:
		return redirect(url_for('login'))
	orders = []
	if request.method == 'POST':
		number = request.form.get('number')
		refund_str = get_result("refund_ticket -u {} -n {}".format(session['C_USER'], number))
		flash('Success. Order '+ number+' has been refunded.')
		return redirect(url_for('query_order'))
	username = session['C_USER']
	orders_str = get_result("query_order -u {}".format(session['C_USER']))
	q_order_display = 'display:block'
	for order_str in orders_str.split('\n'):
		if order_str == '':
			continue
		if orders_str.index(order_str) == 0:
					num = order_str
					continue
		bought_ticket = Order_()
		[bought_ticket.status, bought_ticket.id_, bought_ticket.from_, bought_ticket.from_date, bought_ticket.from_time, bought_ticket.none_, bought_ticket.to, bought_ticket.to_date, bought_ticket.to_time, bought_ticket.price, bought_ticket.num] = order_str.split(' ')
		if bought_ticket.status == "[refunded]":
			bought_ticket.disabled = "disabled"
			bought_ticket.color = "grey"
		bought_ticket.status = bought_ticket.status.split('[')[1]
		bought_ticket.status = bought_ticket.status.split(']')[0]
		orders.append(bought_ticket)
	return render_template('query_order.html', C_USER=session['C_USER'], P=session['P'], orders=orders, q_order_display=q_order_display, num=num)

@app.route('/buy.html', methods=['GET','POST'])
def buy():
	if not 'C_USER' in session:
		return redirect(url_for('login'))
	id_v=month_v=date_v=number_v=account_v=from_v=to_v =''
	m_max = 8
	m_min = 6
	d_max = 31
	d_min = 1
	s_max = 100000
	if request.method == 'POST':
		if 'buy' in request.form:
			train_id = request.form.get('train_id')
			from_ = request.form.get('from')
			to_= request.form.get('to')
			date_min = request.form.get('d_min')
			date_min = date_min.split('-')
			m_min = int(date_min[0])
			d_min = int(date_min[1])
			number_v = month_v = date_v = account_v = ''
			return render_template('buy.html', C_USER=session['C_USER'], P=session['P'], number_v=number_v, id_v=train_id ,month_v=m_min,date_v=d_min,account_v=account_v,from_v=from_,to_v=to_,m_max = m_max, m_min = m_min,d_max = d_max,d_min = d_min,s_max = s_max)
		id_ = request.form.get('id')
		from_ = request.form.get('from')
		to = request.form.get('to')
		month = request.form.get('month')
		date = request.form.get('date')
		number = request.form.get('number')
		account = request.form.get('account')
		id__ = id_check_valid(id_)
		if id__ == '!':
			flash('Invalid input: "'+ id_ +'". (A valid train id should be a string with an initial letter and made up of letter(s), number(s) or underline(s).)')
			return render_template('buy.html', C_USER=session['C_USER'], P=session['P'], number_v=number, id_v=id_,month_v=month,date_v=date,account_v=account,from_v=from_,to_v=to,m_max = m_max, m_min = m_min,d_max = d_max,d_min = d_min,s_max = s_max)
		if not check_station_name(from_, 1) :
			flash('Invalid input: "'+ from_ +'". 站名应为不超过十个汉字组成。')
			return render_template('buy.html', C_USER=session['C_USER'], P=session['P'], number_v=number, id_v=id_,month_v=month,date_v=date,account_v=account,from_v=from_,to_v=to,m_max = m_max, m_min = m_min,d_max = d_max,d_min = d_min,s_max = s_max)
		if not check_station_name(to, 1):
			flash('Invalid input: "'+ to +'". 站名应为不超过十个汉字组成。')
			return render_template('buy.html', C_USER=session['C_USER'], P=session['P'], number_v=number, id_v=id_,month_v=month,date_v=date,account_v=account,from_v=from_,to_v=to,m_max = m_max, m_min = m_min,d_max = d_max,d_min = d_min,s_max = s_max)
		if not check_date(month, date):
			flash('Invalid input: '+ month+'-'+date +'.')
			return render_template('buy.html', C_USER=session['C_USER'], P=session['P'], number_v=number, id_v=id_,month_v=month,date_v=date,account_v=account,from_v=from_,to_v=to,m_max = m_max, m_min = m_min,d_max = d_max,d_min = d_min,s_max = s_max)
		date_ = form_date(month, date)
		if account == "若余票不足，我接受候补购票。":
			account_ = "true"
		else:
			account_ = "false"
		buy_str = get_result("buy_ticket -u {} -i {} -d {} -n {} -f {} -t {} -q {}".format(session['C_USER'], id__, date_, number, from_, to, account_))
		if buy_str == '-1':
			flash('Fail. Maybe go to query available ticket first.')
			return render_template('buy.html', C_USER=session['C_USER'], P=session['P'], number_v=number, id_v=id_,month_v=month,date_v=date,account_v=account,from_v=from_,to_v=to,m_max = m_max, m_min = m_min,d_max = d_max,d_min = d_min,s_max = s_max)
		if buy_str == 'queue':
			flash('余票不足，正在排队. Check your status in \'My Order\'.')
			return render_template('buy.html', C_USER=session['C_USER'], P=session['P'], number_v=number_v, id_v=id_v,month_v=month_v,date_v=date_v,account_v=account_v,from_v=from_v,to_v=to_v,m_max = m_max, m_min = m_min,d_max = d_max,d_min = d_min,s_max = s_max)
		flash('支付成功：'+buy_str+' yuan. Confirm your purchase in \'My Order\'.')
		global total_sale
		total_sale += int(buy_str)
	return render_template('buy.html', C_USER=session['C_USER'], P=session['P'], number_v=number_v, id_v=id_v,month_v=month_v,date_v=date_v,account_v=account_v,from_v=from_v,to_v=to_v,m_max = m_max, m_min = m_min,d_max = d_max,d_min = d_min,s_max = s_max)

@app.route('/clear.html', methods=['GET', 'POST'])
def clear():
	if not 'C_USER' in session:
		return redirect(url_for('login'))
	if request.method == 'POST':
		get_result("clean")
		session.pop('C_USER')
		global user_num, total_sale, train_num, released_num
		user_num=total_sale=train_num= released_num=0
		return redirect(url_for('register'))
	return render_template('clear.html', C_USER=session['C_USER'], P=session['P'])

app.secret_key = 'no secret'