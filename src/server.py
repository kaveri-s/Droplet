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
        with Database() as db:
            query = 'select assignmentId, ui, title, semester, teaches.section, courseName, submission from user, teaches, assignment, course where assignment.teachesId=teaches.teachesId and teaches.userId=user.userId and teaches.courseId=course.courseId and user.userId=%s'
            params =(session['pid']) 
            db.execute(query,params)
            results = db.fetchall()
            col = db.description()
            data = [dict(zip(col, row)) for row in results]
            if(data['ui']=='web'):
                query = 'select * from web where assignmentId=%s'
                params =(data['assignmentId'])
                db.execute(query,params)
                results = db.fetchall()
                col = db.description()
                sub = [dict(zip(col, row)) for row in results]
                data['web'] = sub
            elif(data['ui']=='rest'):
                query = 'select * from rest where assignmentId=%s'
                params =(data['assignmentId'])
                db.execute(query,params)
                results = db.fetchall()
                col = db.description()
                sub = [dict(zip(col, row)) for row in results]
                data['rest'] = sub
            else:
                query = 'select * from cli where assignmentId=%s'
                params =(data['assignmentId'])
                db.execute(query,params)
                results = db.fetchall()
                col = db.description()
                sub = [dict(zip(col, row)) for row in results]
                data['rest'] = sub
        return render_template('prof_viewAssignment.html', name = session["name"], **data)
    else:
        return render_template('index.html')

@app.route('/professor/create/assignment')
def createAssigment():
    if 'p_id' in session:
        return render_template('prof_create.html', name = session["name"])
    else:
        return render_template('index.html')

@app.route('/professor/create/assignment/confirm',methods=['POST'])
def createAssigmentConfirm():
    #if 'p_id' in session:
    if True:
        print(request.is_json)
        content=request.json
        print(content)
        title = content['title']
        description = content['description']
        database = content['database']
        ui=content['ui']
        submission=content['submission']
        with Database() as db:
            query = 'select teachesId from course,teaches where semester=%s and section=%s and coursename=%s and course.courseId=teaches.courseId;'
            params = ([content['semester'], content['section'], content['course']])
            db.execute(query,params)
            results = db.fetchone()
            query = 'insert into assignment(title,descr,db,ui,submission,teachesId) values (%s,%s,%s,%s,%s,%s);'
            params =([title,description,database,ui,submission,results[0]])
            db.execute(query,params)
            query = 'select assignmentId from assignment where title=%s and descr=%s and db=%s and ui=%s and submission =%s and teachesId=%s'
            params =([title,description,database,ui,submission,results[0]])
            db.execute(query,params)
            results = db.fetchone()
            if(content['ui']=='web'):
                for web in content['web']:
                    query = 'insert into web values(%s,%s,%s)'
                    params =(web['testno'], web['scenario'],content['assignmentId'])
                    db.execute(query,params)
                    data = "Success"
            elif(content['ui']=='rest'):
                for rest in content['web']:
                    query = 'insert into rest values(%s,%s, %s, %s, %s)'
                    params =(rest['testno'], rest['api'], rest['method'], rest['statusCode'], content['assignmentId'])
                    db.execute(query,params)
                    data = "Success"
            else:
                query = 'insert into cli values (execname,params,assignmentId)'
                params =(content['execname'], content['params'],content['assignmentId'])
                db.execute(query,params)
                data = "Success"
        return json.dumps(data)
    else:
        return render_template('index.html')

@app.route('/professor/get/<assignment_id>/<submission_id>')
def getSubmissions(assignment_id, submission_id):
    if 'p_id' in session:
        with Database() as db:
            query = 'select * from submission where submissionId=%s;'
            params =([submission_id])
            db.execute(query,params)
            results= db.fetchall()
            col = db.description()
            data = [dict(zip(col, row)) for row in results]

        return render_template('prof_viewSubmission.html', name = session["name"], **data)
    else:
        return render_template('index.html')

####
# Student Functions
####

@app.route('/student/get/<assignment_id>')
def getSubmission(assignment_id):
    if 's_id' in session:
        with Database() as db:
            query = 'select * from assignment where assignmentId=%s;'
            params =([assignment_id]) 
            db.execute(query,params)
            results = db.fetchall()
            col = db.description()
            data = [dict(zip(col, row)) for row in results]
        return render_template('stu_submission.html', name = session["name"], **data)
    else:
        return render_template('index.html') 

@app.route('/student/create/submission')
def createSubmission():
    if 's_id' in session:
        return render_template('stu_submit.html', name = session["name"])
    else:
        return render_template('index.html')

@app.route('/student/create/submission/confirm',methods=["POST"])
def createSubmissionConfirm():
    if 's_id' in session:
        print(request.is_json)
        content=request.json
        print(content)
        gitlink = content['gitink']
        doclink = content['doclink']
        toolpath=content['toolpath']
        reportlink=content['reportlink']
        host=content['host']
        port=content['port']
        takesid=content['takesid']
        assignmentid=content['assignmentid']
        
        with Database() as db:
            query = 'insert into submission(gitlink,doclink,toolpath,reportlink,host,port,takesid,assignmentid) values (%s,%s,%s,%s,%s,%s,%s,%s);'
            params =([gitlink,doclink,toolpath,reportlink,host,port,takesid,assignmentid]) 
            db.execute(query,params)
            data="success"
        return json.dumps(data)
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








