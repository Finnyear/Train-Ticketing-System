from flask import Flask, render_template

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

@app.route('/release.html')
def release():
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
	return render_template('query_order.html')

@app.route('/query_tickets.html')
def query_tickets():
	return render_template('query_tickets.html')

@app.route('/query_train.html')
def query_train():
	return render_template('query_train.html')

@app.route('/query_user.html')
def query_user():
	return render_template('query_user.html')