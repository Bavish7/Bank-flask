from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import random
import MySQLdb.cursors
import re
from datetime import date

app = Flask(__name__)


app.secret_key = 'your secret key'


app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'bavish82'
app.config['MYSQL_DB'] = 'bank'


mysql = MySQL(app)



@app.route('/login.logincontent', methods =['GET', 'POST'])
def login():
	msg = ''
	if request.method == 'POST' and 'email' in request.form and 'passwd' in request.form:
		email = request.form['email']
		passwd = request.form['passwd']
		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute('SELECT * FROM user_table WHERE email = % s AND passwd = % s', (email, passwd, ))
		account = cursor.fetchone()
		if account:
			session['loggedin'] = True
			session['email'] = account['email']
			msg = 'LOGGED IN SUCCESSFULLY !'
			return redirect(url_for('home',session=True))
		else:
			msg = 'INCORRECT EMAIL/PASSWORD !'
	return render_template('login.html', msg = msg)

@app.route('/login.registercontent', methods =['GET', 'POST'])
def register():
	msg1= ''
	if request.method == 'POST' and 'email' in request.form and 'passwd' in request.form:
		email = request.form['email']
		passwd = request.form['passwd']
		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute('SELECT * FROM user_table WHERE email = % s', (email, ))
		account = cursor.fetchone()
		if account:
			msg1 = 'ACCOUNT ALREADY EXISTS !'
		elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
			msg1 = 'INVALID EMAIL ADDRESS !'
		elif len(passwd)!=4:
			msg1 = 'PLEASE ENTER 4-DIGIT PIN !'
		else:
			cursor.execute('INSERT INTO user_table VALUES (% s, % s)', (email, passwd, ))
			mysql.connection.commit()
			msg1 = 'SUCCESS! PLEASE LOGIN'
			return render_template('login.html', msg1 = msg1)
	elif request.method == 'POST':
		msg1 = 'PLEASE FILL OUT THE FORM !'
	return render_template('login.html', msg1 = msg1)

@app.route('/')
@app.route("/home")
def home():
	if 'loggedin' in session:
		return render_template("home.html",session=True)
	return render_template('home.html',session=False)

@app.route("/services")
def services():
	if 'loggedin' in session:
		return render_template("services.html")
	return redirect(url_for('login'))

@app.route("/savings", methods=['GET','POST'])
def savings():
	if 'loggedin' in session:
		msg = ''
		if request.method == 'POST' and 'email' in request.form and 'pin' in request.form and 'acct_name' in request.form and 'phone_no' in request.form and 'address' in request.form and 'current_amt' in request.form :
			email = request.form['email']
			pin = request.form['pin']
			acct_no=random.randrange(1000000000,9999999999)
			acct_name=request.form['acct_name']
			phone_no=request.form['phone_no']
			address=request.form['address']
			current_amt=request.form['current_amt']
			cursor = mysql.connection.cursor()
			cursor.execute('SELECT * FROM cust_details WHERE email = % s', (email,))
			account = cursor.fetchone()
			if account:
				msg = 'EMAIL ID ALREADY EXISTS !'
			elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
				msg = 'INVALID EMAIL ADDRESS !'
			elif len(pin)!=4:
				msg = 'PLEASE ENTER 4-DIGIT TRANSACTION PIN !'
			elif session['email']!=email:
				msg = 'PLEASE ENTER SAME EMAIL !'
			else:
				cursor.execute('INSERT INTO cust_details VALUES (%s, %s, %s, %s, %s, %s, %s, %s)', (email, acct_no, pin, "savings",acct_name, phone_no, address, current_amt ))
				mysql.connection.commit()
				cursor.execute("select acct_no from cust_details where email=%s",(email,))
				row=cursor.fetchone()
				for acct_no in row:
					continue
				msg = 'YOUR ACCOUNT NUMBER IS :'
				return render_template("savings.html",acct_no=acct_no,msg=msg)
		elif request.method == 'POST':
			msg = 'PLEASE FILL OUT THE FORM !'
		return render_template('savings.html', msg = msg)
	return redirect(url_for('login'))

@app.route("/current", methods=['GET','POST'])
def current():
	if 'loggedin' in session:
		msg = ''
		if request.method == 'POST' and 'email' in request.form and 'pin' in request.form and 'acct_name' in request.form and 'phone_no' in request.form and 'address' in request.form and 'current_amt' in request.form :
			email = request.form['email']
			pin = request.form['pin']
			acct_no=random.randrange(1000000000,9999999999)
			acct_name=request.form['acct_name']
			phone_no=request.form['phone_no']
			address=request.form['address']
			current_amt=request.form['current_amt']
			cursor = mysql.connection.cursor()
			cursor.execute('SELECT * FROM cust_details WHERE email = % s', (email, ))
			account = cursor.fetchone()
			if account:
				msg = 'EMAIL ID ALREADY EXISTS !'
			elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
				msg = 'INVALID EMAIL ADDRESS !'
			elif len(pin)!=4:
				msg = 'PLEASE ENTER 4-DIGIT TRANSACTION PIN !'
			elif session['email']!=email:
				msg = 'PLEASE ENTER SAME EMAIL !'
			else:
				cursor.execute('INSERT INTO cust_details VALUES (%s, %s, %s, %s, %s, %s, %s, %s)', (email, acct_no, pin, "current",acct_name, phone_no, address, current_amt ))
				mysql.connection.commit()
				cursor.execute("select acct_no from cust_details where email=%s",(email,))
				row=cursor.fetchone()
				for acct_no in row:
					continue
				msg = 'YOUR ACCOUNT NUMBER IS :'
				return render_template("current.html",acct_no=acct_no,msg=msg)
		elif request.method == 'POST':
			msg = 'PLEASE FILL OUT THE FORM !'
		return render_template('current.html', msg = msg)
	return redirect(url_for('login'))



@app.route("/upi", methods=['GET','POST'])
def upi():
	if 'loggedin' in session:
		msg = ''
		if request.method == 'POST' and 'email_id' in request.form and 'amt' in request.form and 'pin' in request.form 	:
			email = session['email']
			pin = request.form['pin']
			cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
			cursor.execute('SELECT * FROM cust_details WHERE email = %s and pin = %s', (email, pin, ))
			account=cursor.fetchone()
			if account:
				email_id = request.form['email_id']
				cursor.execute("SELECT acct_name from cust_details WHERE email = %s",(email_id, ))
				row=cursor.fetchone()
				for name in row.values():
					continue
				cursor.execute("SELECT acct_name from cust_details WHERE email = %s",(email, ))
				row1=cursor.fetchone()
				for name1 in row1.values():
					continue
				if name is None:
					msg='INVALID EMAIL ID !'
				else:
					from datetime import date
					amt=request.form['amt']
					try:
						cursor.execute("UPDATE cust_details SET current_amt = current_amt - %s WHERE email= %s",(amt,email,))
						cursor.execute("UPDATE cust_details SET current_amt = current_amt + %s WHERE email= %s",(amt,email_id,))
						today=date.today()
						cursor.execute("INSERT into transaction VALUES(%s, %s, %s, %s, %s, NULL, NULL)",(email, "upi", today, amt, name))
						cursor.execute("INSERT into transaction VALUES(%s, %s, %s, NULL, NULL, %s, %s)",(email_id, "upi", today, amt, name1))
						mysql.connection.commit()
						msg="TRANSACTION SUCCESSFUL !"
						return redirect(url_for('services'))
					except:
						msg='INSUFFICIENT BALANCE !'
			else:
				msg = 'INAVLID PIN !'			
		elif request.method == 'POST':
			msg = 'PLEASE FILL OUT THE FORM !'
		return render_template('upi.html', msg = msg)
	return redirect(url_for('login'))

@app.route("/mobile", methods=['GET','POST'])
def mobile():
	if 'loggedin' in session:
		msg = ''
		if request.method == 'POST' and 'phone_no' in request.form and 'amt' in request.form and 'pin' in request.form 	:
			email = session['email']
			pin = request.form['pin']
			cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
			cursor.execute('SELECT * FROM cust_details WHERE email = %s and pin = %s', (email, pin, ))
			account=cursor.fetchone()
			if account:
				phone_no = request.form['phone_no']
				cursor.execute("SELECT acct_name,email from cust_details WHERE phone_no = %s",(phone_no, ))
				row=cursor.fetchone()
				array=list(row.values())
				name=array[0]
				email_id=array[1]
				cursor.execute("SELECT acct_name from cust_details WHERE email = %s",(email, ))
				row1=cursor.fetchone()
				for name1 in row1.values():
					continue
				if name is None:
					msg='INVALID EMAIL ID !'
				else:
					from datetime import date
					amt=request.form['amt']
					try:
						cursor.execute("UPDATE cust_details SET current_amt = current_amt - %s WHERE email= %s",(amt,email,))
						cursor.execute("UPDATE cust_details SET current_amt = current_amt + %s WHERE phone_no= %s",(amt,phone_no,))
						today=date.today()
						cursor.execute("INSERT into transaction VALUES(%s, %s, %s, %s, %s, NULL, NULL)",(email, "mobile", today, amt, name))
						cursor.execute("INSERT into transaction VALUES(%s, %s, %s, NULL, NULL, %s, %s)",(email_id, "mobile", today, amt, name1))
						mysql.connection.commit()
						msg="TRANSACTION SUCCESSFUL !"
						return redirect(url_for('services'))
					except:
						msg='INSUFFICIENT BALANCE !'
			else:
				msg = 'INAVLID PIN !'			
		elif request.method == 'POST':
			msg = 'PLEASE FILL OUT THE FORM !'
		return render_template('mobile.html', msg = msg)
	return redirect(url_for('login'))

@app.route("/bank", methods=['GET','POST'])
def bank():
	if 'loggedin' in session:
		msg = ''
		if request.method == 'POST' and 'acct_no' in request.form and 'amt' in request.form and 'pin' in request.form 	:
			email = session['email']
			pin = request.form['pin']
			cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
			cursor.execute('SELECT * FROM cust_details WHERE email = %s and pin = %s', (email, pin, ))
			account=cursor.fetchone()
			if account:
				acct_no = request.form['acct_no']
				cursor.execute("SELECT acct_name,email from cust_details WHERE acct_no = %s",(acct_no, ))
				row=cursor.fetchone()
				array=list(row.values())
				name=array[0]
				email_id=array[1]
				cursor.execute("SELECT acct_name from cust_details WHERE email = %s",(email, ))
				row1=cursor.fetchone()
				for name1 in row1.values():
					continue
				if name is None:
					msg='INVALID EMAIL ID !'
				else:
					from datetime import date
					amt=request.form['amt']
					try:
						cursor.execute("UPDATE cust_details SET current_amt = current_amt - %s WHERE email= %s",(amt,email,))
						cursor.execute("UPDATE cust_details SET current_amt = current_amt + %s WHERE acct_no= %s",(amt,acct_no,))
						today=date.today()
						cursor.execute("INSERT into transaction VALUES(%s, %s, %s, %s, %s, NULL, NULL)",(email, "bank", today, amt, name))
						cursor.execute("INSERT into transaction VALUES(%s, %s, %s, NULL, NULL, %s, %s)",(email_id, "bank", today, amt, name1))
						mysql.connection.commit()
						msg="TRANSACTION SUCCESSFUL !"
						return redirect(url_for('services'))
					except:
						msg='INSUFFICIENT BALANCE !'
			else:
				msg = 'INAVLID PIN !'			
		elif request.method == 'POST':
			msg = 'PLEASE FILL OUT THE FORM !'
		return render_template('bank.html', msg = msg)
	return redirect(url_for('login'))

@app.route("/display")
def display():
	if 'loggedin' in session:
		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute('SELECT * FROM cust_details WHERE email = % s', (session['email'], ))
		account = cursor.fetchone()
		return render_template("display.html", account = account)
	return redirect(url_for('login'))

@app.route("/update", methods =['GET', 'POST'])
def update():
	msg = ''
	if 'loggedin' in session:
		if request.method == 'POST' and 'pin' in request.form and 'npin' in request.form and 'phone_no' in request.form and 'address' in request.form:
			email=session['email']
			pin= request.form['pin']
			npin=request.form['npin']
			phone_no= request.form['phone_no']
			address= request.form['address']
			cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
			cursor.execute('SELECT * FROM cust_details WHERE email = % s and pin = %s', (email,pin, ))
			account = cursor.fetchone()
			if len(npin)!=4:
				msg = 'PLEASE ENTER 4-DIGIT TRANSACTION PIN !'
			elif account:
				cursor.execute('update cust_details set pin = %s, phone_no= %s , address= %s where email= %s',(npin,phone_no,address,email,))
				mysql.connection.commit()
				msg = 'SUCCESSFULLY UPDATED !'
			else:
				msg= 'INVALID PIN !'
		elif request.method == 'POST':
			msg = 'PLEASE FILL OUT THE FORM !'
		return render_template("update.html", msg = msg)
	return redirect(url_for('login'))

@app.route("/all_transactions", methods=['GET','POST'])
def all_transactions():
	if 'loggedin' in session:
		output=False
		msg = ''
		if request.method == 'POST' and 'pin' in request.form 	:
			email = session['email']
			pin = request.form['pin']
			cursor = mysql.connection.cursor()
			cursor.execute('SELECT * FROM cust_details WHERE email = %s and pin = %s', (email, pin, ))
			account=cursor.fetchone()
			if account:
				cursor.execute("SELECT * from transaction WHERE email = %s order by date desc",(email, ))
				data=cursor.fetchall()
				output=True
				msg = 'TRANSACTION SUCCESSFUL !'
				return render_template('output.html',output_data=data, output=True)
			else:
				msg='INVALID PIN !'
		elif request.method == 'POST':
			msg = 'PLEASE FILL OUT THE FORM !'
		return render_template("all_transactions.html", msg = msg)
	return render_template(url_for("login"))

@app.route("/last_transactions", methods=['GET','POST'])
def last_transactions():
	if 'loggedin' in session:
		output=False
		msg = ''
		if request.method == 'POST' and 'pin' in request.form :
			email = session['email']
			pin = request.form['pin']
			cursor = mysql.connection.cursor()
			cursor.execute('SELECT * FROM cust_details WHERE email = %s and pin = %s', (email, pin, ))
			account=cursor.fetchone()
			if account:
				cursor.execute("SELECT * from transaction WHERE email = %s order by date desc",(email, ))
				data=cursor.fetchmany(10)
				output=True
				msg = 'TRANSACTION SUCCESSFUL !'
				return render_template('last-output.html',output_data=data, output=True)
			else:
				msg='INVALID PIN !'
		elif request.method == 'POST':
			msg = 'PLEASE FILL OUT THE FORM !'
		return render_template("last_transactions.html", msg = msg)
	return render_template(url_for("login"))

@app.route('/date', methods=['GET','POST'])
def date():
	if 'loggedin' in session:
		output=False
		msg = ''
		if request.method == 'POST' and 'pin' in request.form and 'start' in request.form and 'end' in request.form:
			email = session['email']
			pin = request.form['pin']
			start=request.form['start']
			end=request.form['end']
			cursor = mysql.connection.cursor()
			cursor.execute('SELECT * FROM cust_details WHERE email = %s and pin = %s', (email, pin, ))
			account=cursor.fetchone()
			if account:
				cursor.execute("SELECT * from transaction WHERE email = %s and date between %s and %s order by date desc",(email, start, end, ))
				data=cursor.fetchall()
				output=True
				msg = 'TRANSACTION SUCCESSFUL !'
				return render_template('output.html',output_data=data, output=True)
			else:
				msg='INVALID PIN !'
		elif request.method == 'POST':
			msg = 'PLEASE FILL OUT THE FORM !'
		return render_template("date.html", msg = msg)
	return render_template(url_for("login"))

@app.route("/credit_score", methods=['GET','POST'])
def credit_score():
	if 'loggedin' in session:
		msg = ''
		if request.method == 'POST' and 'pin' in request.form and 'age' in request.form and 'home' in request.form and 'income' in request.form and 'credit' in request.form and 'year' in request.form and 'delay' in request.form :
			email = session['email']
			pin = request.form['pin']
			age=request.form['age']
			for age in range(20,40):
				score=int(age)*4.5
				for age in range(40,50):
					score=int(age)*3.2
				for age in range(50,56):
					score=int(age)*2
				else :
					score=90
			home=request.form['home']
			if home=="y" :
				score+=200
			else :
				score+=90
			income=request.form['income']
			if int(income)<500000 :
				score+=80
			elif int(income) in range(500000,1000000):
				score+=100
			elif int(income) in range(1000000,1500000):
				score+=150
			elif int(income) in range(1500000,2000000):
				score+=200
			else:
				score+=250
			credit=request.form['credit']
			score+=int(credit)*10
			year=request.form['year']
			score+=int(year)*10
			delay=request.form['delay']
			score-=int(delay)*10
			cursor = mysql.connection.cursor()
			cursor.execute('SELECT * FROM cust_details WHERE email = %s and pin = %s', (email, pin, ))
			account=cursor.fetchone()
			if account:
				msg1="YOUR CREDIT SCORE IS : "
				return render_template('credit_score.html',score=score,msg1=msg1)
			else:
				msg='INVALID PIN !'
		elif request.method == 'POST':
			msg = 'PLEASE FILL OUT THE FORM !'		
		return render_template("credit_score.html", msg = msg)
	return render_template(url_for("login"))

@app.route("/delete", methods=['GET','POST'])
def delete():
	if 'loggedin' in session:
		msg=''
		if request.method == 'POST' and 'pin' in request.form and 'delete' in request.form:
			email=session['email']
			pin=request.form['pin']
			cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
			cursor.execute("select * from cust_details where email= %s and pin= %s",(email,pin,))
			account=cursor.fetchone()
			if account:
				delete=request.form['delete']
				if ((delete == "Yes") or (delete == "yes") or (delete == "YES")):
					cursor.execute("delete from cust_details where email= %s",(email,))
					mysql.connection.commit()
					msg='ACCOUNT DELETED SUCCESSFULLY !'
					return render_template('delete.html',msg=msg)
				else :
					return redirect(url_for('home'))
			else:
				msg='INVALID PIN !'
		elif request == 'POST':
			msg='PLEASE FILL OUT THE FORM !'
		return render_template("delete.html",msg=msg)
	return render_template(url_for('login'))

@app.route("/help")
def help():
	return render_template("help.html")

@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('email', None)
    return render_template('home.html',session=False)

if __name__ == "__main__":
	app.run(host ="localhost", port = int("5000"))
