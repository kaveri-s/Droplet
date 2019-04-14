import os, os.path
import glob
from database import *
import datetime

# Database related Utilities
def validate(data):
    with Database() as db:
        db.execute('select * from user where userId=%s and email=%s and pass=%s and userrole=%s',([data["usn"], data["email"], data["password"], data["role"]]))
        results = db.fetchall()
    return results

# Get list of assignments
def getAssignments(id, action):
    with Database() as db:
        query = 'select assignmentId, title, semester, section, courseName, submission from user, '+action+', assignment, course where assignment.'+action+'Id='+action+'.'+action+'Id and '+action+'.userId=user.userId and '+action+'.courseId=course.courseId and user.userId=%s order by submission desc'
        params =([id])
        db.execute(query,params)
        results = db.fetchall()
        col = db.description()
        data = [dict(zip(col, row)) for row in results]
    return data

#Get one Assignment
def getAssignment(assignment_id):
    with Database() as db:
        query = 'select assignmentId, descr, db, ui, title, semester, section, courseName, submission from user, teaches, assignment, course where assignment.teachesId=teaches.teachesId and teaches.userId=user.userId and teaches.courseId=course.courseId and assignmentId=%s'
        params =([assignment_id]) 
        db.execute(query,params)
        results = db.fetchone()
        col = db.description()
        data = dict(zip(col, results))
        data['submission'] = data['submission'].strftime('%d/%m/%Y')
        data['no_tests'] = get_num_files('../tests/1/cases/')
    return data

# Get details of Web based assignments
def getWeb(assignment_id, pid):
    with Database() as db:
        query = 'select * from web where assignmentId=%s'
        params =([assignment_id])
        db.execute(query,params)
        results = db.fetchall()
        col = db.description()
        data = [dict(zip(col, row)) for row in results]
    return data

# Get Details of Rest based assignments
def getRest(assignment_id, pid):
    with Database() as db:
        query = 'select * from rest where assignmentId=%s'
        params =([assignment_id])
        db.execute(query,params)
        results = db.fetchall()
        col = db.description()
        data = [dict(zip(col, row)) for row in results]
    return data

# Get details of CUI based assignments
def getCui(assignment_id, pid):
    with Database() as db:
        query = 'select * from cui where assignmentId=%s'
        params =([assignment_id])
        db.execute(query,params)
        results = db.fetchall()
        col = db.description()
        data = [dict(zip(col, row)) for row in results]
    return data

# Get all submissions of an assignment
def getSubmissions(assignment_id):
    with Database() as db:
        query = 'select * from submission where submissionId=%s;'
        params =([assignment_id])
        db.execute(query,params)
        results= db.fetchall()
        col = db.description()
        data = [dict(zip(col, row)) for row in results]
    return data

# get one submission
def getSubmission(submission_id):
    with Database() as db:
        query = 'select * from submission where submissionId=%s;'
        params =([submission_id]) 
        db.execute(query,params)
        results = db.fetchall()
        col = db.description()
        data = [dict(zip(col, row)) for row in results]
    return data

# create an assignment
def createAssignmentConfirm(data, pid):
    with Database() as db:
        query = 'select teachesId from course,teaches where semester=%s and section=%s and coursename=%s and course.courseId=teaches.courseId;'
        params = ([data['semester'], data['section'], data['course']])
        db.execute(query,params)
        results = db.fetchone()
        query = 'insert into assignment(title,descr,db,ui,submission,teachesId) values (%s,%s,%s,%s,%s,%s);'
        params =([data['title'],data['description'],data['database'],data['ui'],data['submission'],results[0]])
        db.execute(query,params)
        query = 'select assignmentId from assignment where title=%s and descr=%s and db=%s and ui=%s and submission =%s and teachesId=%s'
        params =([data['title'],data['description'],data['database'],data['ui'],data['submission'],results[0]])
        db.execute(query,params)
        results = db.fetchone()
        if(data['ui']=='web'):
            for web in data['web']:
                query = 'insert into web values(%s,%s,%s)'
                params =(web['testno'], web['scenario'],data['assignmentId'])
                db.execute(query,params)
                return "Success"
        elif(data['ui']=='rest'):
            for rest in data['web']:
                query = 'insert into rest values(%s,%s, %s, %s, %s)'
                params =(rest['testno'], rest['api'], rest['method'], rest['statusCode'], data['assignmentId'])
                db.execute(query,params)
                return "Success"
        else:
            query = 'insert into cui values (execname,params,assignmentId)'
            params =(data['execname'], data['params'],data['assignmentId'])
            db.execute(query,params)
            return "Success"


# Create a submission
def createSubmissionConfirm(data, sid):
    with Database() as db:
        query = 'insert into submission(gitlink,doclink,toolpath,reportlink,host,port,takesid,assignmentid) values (%s,%s,%s,%s,%s,%s,%s,%s);'
        params =([data['gitink'],data['doclink'],data['toolpath'],data['reportlink'],data['host'],data['port'],data['takesid'],data['assignmentid']]) 
        db.execute(query,params)
        return "Success"

# File related Utilities
def get_num_files(path):
    return len(glob.glob1(path,"ip*"))

print(getAssignment(1))