from flask import Flask, render_template, request, redirect, flash, url_for
from mine import *

app = Flask(__name__)

@app.route('/')
@app.route('/index.html')
def index():
	return render_template('index.html')

@app.route('/add_train.html')
def add_train():
	return render_template('add_train.html')

@app.route('/add user.html')
def add_user():
	return render_template('add user.html')

@app.route('/buy.html')
def buy():
	return render_template('buy.html')

@app.route('/clear.html')
def clear():
	return render_template('clear.html')

@app.route('/delete.html')
def delete():
	return render_template('delete.html')

@app.route('/release.html', methods=['GET', 'POST'])
def release():
	if request.method == 'POST':
		train_id = request.form.get('train_id')
		train_id_ = id_check_valid(train_id)
		if train_id_ == '!':
			flash('Invalid input: "'+ train_id +'". (A valid train ID should be a string with an initial letter and made up of letter(s), number(s) or underline(s).)')
			return redirect(url_for('release'))
		#将train_id_送到后台并接受返回信息
		if train_id_ == 'cht':
			train_id_str = '0'
		else:
			train_id_str = '-1'
		###############################	
		if train_id_str == '-1':
			flash('Fail. Maybe go to check the train info first.')
			return redirect(url_for('release'))

		flash('Success.')
		return redirect(url_for('release'))

	return render_template('release.html')

@app.route('/refund.html')
def refund():
	return render_template('refund.html')

@app.route('/login.html')
def login():
	return render_template('login.html')

@app.route('/register.html')
def register():
	return render_template('register.html')

@app.route('/query_order.html')
def query_order():
	orders_str = 'IS PENDING|CHT|Shanghai|12-21 |13:23|12-21 |13:23|Beijing|100|50\nIS PENDING|CHT|Shanghai|12-21 |13:23|12-21 |13:23|Beijing|100|50'
	orders = []
	for order_str in orders_str.split('\n'):
		bought_ticket = Order_()
		[bought_ticket.status, bought_ticket.id_, bought_ticket.from_, bought_ticket.from_date, bought_ticket.from_time, bought_ticket.to, bought_ticket.to_date, bought_ticket.to_time, bought_ticket.price, bought_ticket.num] = order_str.split('|')
		orders.append(bought_ticket)
	return render_template('query_order.html', orders=orders)

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

@app.route('/query_train.html')
def query_train():
	trains = []
	train_id = 'CHT'
	train_type = 'G'
	trains_str = "Shanghai|xx-xx|xx:xx|12-21 |13:23| 100|50\nNanjing|12-22| 14:23|12-21 |17:53|100|50\nBeijing|12-25 |1:41|xx-xx|xx:xx |100|x"
	for train_str in trains_str.split('\n'):
		train_ = Train_()
		[train_.station, train_.to_date, train_.to_time, train_.from_date, train_.from_time, train_.price, train_.remain] = train_str.split('|')
		trains.append(train_)
	return render_template('query_train.html', trains=trains, train_id=train_id, train_type=train_type)

@app.route('/query_user.html')
def query_user():
	user_str = 'CHT|cht|cht@163.com|5'
	user_ = User_()
	[user_.u_name, user_.name, user_.mail, user_.p_] = user_str.split('|')
	return render_template('query_user.html', user_=user_)

app.secret_key = 'no secret'