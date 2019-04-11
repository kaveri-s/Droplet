from flask import Flask, flash,session, render_template, request, redirect, Response ,jsonify, json, url_for
from database import *

app = Flask(__name__)
app.secret_key = 'droplet'

@app.route('/professor/get/assignments')
def getAssignments():
    #if 'p_id' in session:
    if True:  
        #pid = session["p_id"]
        pid ="P002"
        with Database() as db:
            query = 'select assignmentId, title, semester, teaches.section, courseName, submission from user, teaches, assignment, course where assignment.teachesId=teaches.teachesId and teaches.userId=user.userId and teaches.courseId=course.courseId and user.userId=%s'
            params =([pid]) 
            db.execute(query,params)
            results = db.fetchall()
            col = db.description()
            data = [dict(zip(col, row)) for row in results]
        return json.dumps(data)
    else:
        return render_template('index.html')

@app.route('/professor/create/assignment',methods=['POST'])
def createAssigment():
    #if 'p_id' in session:
    if True:  
        #pid = session["p_id"]
        pid ="P002"
        print(request.is_json)
        content=request.json
        print(content)
        title = content['title']
        description = content['description']
        database = content['database']
        ui=content['ui']
        submission=content['submission']
        teachesId=content['teachesId']
        with Database() as db:
            query = 'insert into assignment(title,descr,db,ui,submission,teachesId) values (%s,%s,%s,%s,%s,%s);'
            params =([title,description,database,ui,submission,teachesId]) 
            db.execute(query,params)
            data="success"
        return json.dumps(data)
    else:
        return render_template('index.html')

@app.route('/professor/get/<assignment_id>')
def getAssignment(assignment_id):
    #if 'p_id' in session:
    if True:  
        #pid = session["p_id"]
        pid ="P002"

        with Database() as db:
            query = 'select assignmentId, title, semester, section, courseName , descr, db, ui, submission from assignment, teaches, course where assignmentId=%s and assignment.teachesId=teaches.teachesId and teaches.courseId=course.courseId;'
            params =([assignment_id])
            db.execute(query,params)
            results= db.fetchall()
            col = db.description()
            data = [dict(zip(col, row)) for row in results]
        return json.dumps(data)
    else:
        return render_template('index.html')

@app.route('/professor/get/<assignment_id>/<submission_id>')
def getSubmissions(assignment_id, submission_id):
    #if 'p_id' in session:
    if True:  
        #pid = session["p_id"]
        pid ="P002"
        with Database() as db:
            query = 'select * from submission where submissionId=%s;'
            params =([submission_id])
            db.execute(query,params)
            results= db.fetchall()
            col = db.description()
            data = [dict(zip(col, row)) for row in results]
        
        return json.dumps(data)
    else:
        return render_template('index.html')

@app.route('/student/get/<assignment_id>')
def getSubmission(assignment_id):
    #if 'p_id' in session:
    if True:  
        #pid = session["p_id"]
        sid ="S001"
        with Database() as db:
            query = 'select * from assignment where assignmentId=%s;'
            params =([assignment_id]) 
            db.execute(query,params)
            results = db.fetchall()
            col = db.description()
            data = [dict(zip(col, row)) for row in results]
        return json.dumps(data)
    else:
        return render_template('index.html') 


@app.route('/student/create/submission',methods=["POST"])
def createSubmission():
    #if 's_id' in session:
    if True:  
        #sid = session["s_id"]
        sid ="S001"
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



if __name__ == '__main__':
# run!
    app.run(debug=True)