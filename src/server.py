from flask import Flask, flash,session, render_template, request, redirect, Response ,jsonify, json, url_for
from string import Template
from database import *

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
    print(data)
    userId = data["usn"]
    email = data["email"]
    pswd = data["password"]
    role = data["role"]

    with Database() as db:
        db.execute('select * from user where userId=%s and email=%s and pass=%s and userrole=%s',([userId, email, pswd, role]))
        results = db.fetchall()

    if results:
        row = results[0]

        if(row[3] == pswd):
            # do session stuff
            session.clear()
            if(role == "student"):
                session['s_id'] = row[0]
            else:
                session['p_id'] = row[0]
            session['name'] = row[1]
            return "Correct"
        else:
            # wrong password, tell user
            session.clear()
            return "Wrong"
    # If we still reach here, it means that the user is not a registered one
    return "Missing"

#To logout
@app.route('/logout')
def logout():
    if 's_id' in session:
        session.pop('s_id')
        return render_template('index.html')
    elif 'p_id' in session:
        session.pop('p_id')
        return render_template('index.html')
    else:
        return render_template('index.html')

#####
# Main Page
#####
#To display profile page
@app.route('/profile')
def profile():
    if 's_id' in session:
        return render_template('stu_profile.html', name = session["name"])
    elif 'p_id' in session:
        return render_template('prof_profile.html', name = session["name"])
    else:
        return render_template('index.html')

#####
# Prof Pages
#####
@app.route('/professor/get/assignments')
def getAssignments():
    if 'p_id' in session:
        pid = session["p_id"]
        with Database() as db:
            query = 'select assignmentId, title, semester, teaches.section, courseName, submission from user, teaches, assignment, course where assignment.teachesId=teaches.teachesId and teaches.userId=user.userId and teaches.courseId=course.courseId and user.userId=%s order by submission desc'
            params =([pid])
            db.execute(query,params)
            results = db.fetchall()
            col = db.description()
            data = [dict(zip(col, row)) for row in results]
        return json.dumps(data)
    else:
        return render_template('index.html')

@app.route('/professor/get/<assignment_id>')
def getAssignment(assignment_id):
    if 'p_id' in session:
        return render_template('prof_viewAssignment.html', name = session["name"], aid = assignment_id)
    else:
        return render_template('index.html')

@app.route('/professor/create/assignment')
def createAssigment():
    if 'p_id' in session:
        return render_template('prof_create.html', name = session["name"])
    else:
        return render_template('index.html')

@app.route('/professor/get<submission_id>')
def getSubmissions(assignment_id, submission_id):
    if 'p_id' in session:
        return render_template('prof_viewSubmission.html', name = session["name"])
    else:
        return render_template('index.html')

####
# Student Functions
####

@app.route('/student/get/<assignment_id>')
def getSubmission(assignment_id):
    if 's_id' in session:
        return render_template('stu_submission.html', name = session["name"])
    else:
        return render_template('index.html') 

@app.route('/student/create/submission')
def createSubmission():
    if 's_id' in session:
        return render_template('stu_submit.html', name = session["name"])
    else:
        return render_template('index.html')

@app.route('/student/create/dockerfile')
def createDockerfile():
    if 's_id' in session:
        return render_template('stu_dockerfile.html', name = session["name"])
    else:
        return render_template('index.html')

if __name__ == '__main__':
# run!
    app.run(debug=True)








