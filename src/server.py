# Decide whether to use SQLAlchemy (ORM) or MySQLdb (Might have to use a fork, MySQLDb does not have good python3 support)
# For now going with pymysql as it is good enough and very similar to MySQLdb
# Please follow the following naming convention: long_function_name(var_one,var_two)
from flask import Flask, flash,session, render_template, request, redirect, Response ,jsonify, json, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from string import Template
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from itsdangerous import URLSafeSerializer, BadSignature
import pymysql
import smtplib
import datetime

COMPANY_EMAIL_ADDRESS = 'alivedead068@gmail.com'
PASSWORD = 'deadoraliveisasecret'

app = Flask(__name__)
app.secret_key = 'totally a secret lolz'
# db = pymysql.connect("localhost", "wt2", "pass", "Wt2", charset="latin1")

#To display the home page
@app.route('/')
def index():
    if 's_id' in session:
        return render_template('stu_profile.html', name = session["name"])
    elif 'p_id' in session:
        return render_template('prof_profile.html', name = session["name"])
    return render_template('index.html')

#To validate user form data
@app.route('/validate',methods=['POST'])
def validate():
    data = json.loads(request.data)
    usn = data["usn"]
    email = data["email"]
    pswd = data["password"]

    # cursor = db.cursor()
    # sql = "SELECT s_id, s_name, s_email, s_password from student where s_id = %s and s_email = %s"
    # args = ([usn, email])
    # cursor.execute(sql,args)
    # results = cursor.fetchall()
    # cursor.close()
    # print(results)

    results = [['01FB15EC', 'kaveri', 'kaveri.subra@gmail.com', 'kaveri']]

    if results:
        row = results[0]

        if(row[3] == pswd):
            # do session stuff
            session.clear()
            session['s_id'] = row[0]
            session['name'] = row[1]
            return "Correct"
        else:
            # wrong password, tell user
            session.clear()
            return "Wrong"
    # If we still reach here, it means that the user is not a registered one
    return "Missing"

#To display profile page
@app.route('/profile')
def profile():
    if 's_id' in session:
        return render_template('stu_profile.html', name = session["name"])
    elif 'p_id' in session:
        return render_template('prof_profile.html', name = session["name"])
    else:
        return render_template('index.html')

#to get list fo assignments
@app.route('/getList')
def getList():

    return 

#To logout
@app.route('/logout')
def logout():
    if 's_id' in session:
        session.pop('s_id')
        return render_template('index.html')

if __name__ == '__main__':
# run!
    app.run(debug=True)








