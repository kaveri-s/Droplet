import os, os.path
import glob
from database import *
import datetime
import shutil
import rundockers
import json

app_config = json.loads(open('../dropletconfig.json').read())

# Database related Utilities
def validate(data):
    with Database() as db:
        db.execute('select * from user where userId=%s and email=%s and pass=%s and userrole=%s',([data["usn"], data["email"], data["password"], data["role"]]))
        results = db.fetchall()
    return results

# Get list of assignments
def getAssignments(id, role):
    print(id, role)
    with Database() as db:
        query=''
        if(role == "prof"):
            query = 'select assignmentId, title, semester, section, courseName, submission from user, teaches, assignment, course where assignment.teachesId=teaches.teachesId and teaches.userId=user.userId and teaches.courseId=course.courseId and user.userId=%s order by submission desc'
        else:
            query = 'select assignment.assignmentId, title, semester, takes.section, courseName, submission from submission, assignment, teaches, takes, user, course where submission.assignmentId=assignment.assignmentId and assignment.teachesId=teaches.teachesId and submission.takesId=takes.takesId and takes.userId=user.userId and course.courseId=takes.courseId and user.userId=%s order by submission desc'
        print(query)
        params =([id])
        db.execute(query,params)
        results = db.fetchall()
        col = db.description()
        data = [dict(zip(col, row)) for row in results]
        print(data)
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
    return data

# Get details of Web based assignments
def getWeb(assignment_id):
    with Database() as db:
        query = 'select * from web where assignmentId=%s'
        params =([assignment_id])
        db.execute(query,params)
        results = db.fetchall()
        col = db.description()
        data = [dict(zip(col, row)) for row in results]
    return data

# Get Details of Rest based assignments
def getRest(assignment_id):
    with Database() as db:
        query = 'select * from rest where assignmentId=%s'
        params =([assignment_id])
        db.execute(query,params)
        results = db.fetchall()
        col = db.description()
        data = [dict(zip(col, row)) for row in results]
    return data

# Get details of CUI based assignments
def getCui(assignment_id):
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
        query = 'select submissionId, takes.userId from submission, takes where submission.takesId=takes.takesId and assignmentId=%s;'
        params =([assignment_id])
        db.execute(query,params)
        results= db.fetchall()
        col = db.description()
        data = [dict(zip(col, row)) for row in results]
    return data

# get one submission
def getSubmission(assignment_id):
    with Database() as db:
        query = 'select assignment.assignmentId, submissionId, gitLink, dockLink, docLink, ui, takes.userId from submission,assignment,takes where assignment.assignmentId=%s and submission.assignmentId=assignment.assignmentId and submission.takesId=takes.takesId;'
        params =([assignment_id]) 
        db.execute(query,params)
        results = db.fetchall()
        if (len(results)==0):
            data = "Not Submitted"
        else:
            col = db.description()
            data = dict(zip(col, results[0]))
    return data

# get details for creating assignment
def createAssignment(pid):
    with Database() as db:
        #get semesters
        query = 'select semester from teaches, course where teaches.courseId = course.courseId and userId=%s group by semester'
        params =([pid]) 
        db.execute(query,params)
        results = db.fetchall()
        data = [row[0] for row in results]
    return data


def sectionFromSem(pid, semester):
    with Database() as db:
        #get sections
        query = 'select section from teaches, course where teaches.courseId = course.courseId and userId=%s and semester=%s group by section'
        params =([pid, semester]) 
        db.execute(query,params)
        results = db.fetchall()
        data = [row[0] for row in results]
    return data

def courseFromSectionandSem(pid, semester, section):
    with Database() as db:
        #get sections
        query = 'select courseName from teaches, course where teaches.courseId=course.courseId and teaches.userId=%s and semester=%s and section=%s group by courseName'
        params =([pid, semester, section]) 
        db.execute(query,params)
        results = db.fetchall()
        data = [row[0] for row in results]
    return data

# create an assignment
def createAssignmentConfirm(data, pid):
    print(data)
    # with Database() as db:
    #     query = 'select teachesId from course,teaches where semester=%s and section=%s and coursename=%s and course.courseId=teaches.courseId;'
    #     params = ([data['semester'], data['section'], data['course']])
    #     db.execute(query,params)
    #     results = db.fetchone()
    #     query = 'insert into assignment(title,descr,db,ui,submission,teachesId) values (%s,%s,%s,%s,%s,%s);'
    #     params =([data['title'],data['description'],data['database'],data['ui'],data['submission'],results[0]])
    #     db.execute(query,params)
    #     query = 'select assignmentId from assignment where title=%s and descr=%s and db=%s and ui=%s and submission =%s and teachesId=%s'
    #     params =([data['title'],data['description'],data['database'],data['ui'],data['submission'],results[0]])
    #     db.execute(query,params)
    #     results = db.fetchone()
    #     if(data['ui']=='web'):
    #         for testno in range(1, data['testno']+1):
    #             query = 'insert into web values(%s,%s,%s)'
    #             params =(testno, data['scenario'+str(testno)],data['assignmentId'])
    #             db.execute(query,params)
    #             return "Success"
    #     elif(data['ui']=='rest'):
    #         for testno in range(1, data['testno']+1):
    #             query = 'insert into rest values(%s,%s, %s, %s, %s)'
    #             params =(testno, data['api'+str(testno)], data['method'+str(testno)], data['status_code'+str(testno)], data['assignmentId'])
    #             db.execute(query,params)
    #             return "Success"
    #     else:
    #         query = 'insert into cui values (execname,params,assignmentId)'
    #         params =(data['execname'], data['params'],data['assignmentId'])
    #         db.execute(query,params)
    #         return "Success"


# Create a submission
def createSubmissionConfirm(data, sid):
    with Database() as db:
        query = 'select takesId from course,takes where semester=%s and section=%s and coursename=%s and course.courseId=teaches.courseId;'
        params = ([data['semester'], data['section'], data['course']])
        db.execute(query,params)
        results = db.fetchone()
        query = 'insert into submission(gitlink,doclink,toolpath,reportlink,host,port,takesid,assignmentid) values (%s,%s,%s,%s,%s,%s,%s,%s);'
        params =([data['gitink'],data['doclink'],data['toolpath'],data['reportlink'],data['host'],data['port'],results[0],data['assignmentid']]) 
        db.execute(query,params)
        return "Success"

# File related Utilities
def get_num_files(path):
    return len(glob.glob1(path,"ip*"))

# def zip(op, path):
#     shutil.make_archive(op, 'zip', path)

#Docker related utilities
def runDocker(submission_id):
    with Database() as db:
        query = 'select assignment.assignmentId, submissionId, port, ui, dockLink, takes.userId from submission,assignment,takes where submissionId=%s and submission.assignmentId=assignment.assignmentId and submission.takesId=takes.takesId;'
        params =([submission_id]) 
        db.execute(query,params)
        results = db.fetchone()
        col = db.description()
        data = dict(zip(col, results))
        print(data)
        path = app_config["APP_ROOT"]+'tests/'+str(data['assignmentId'])+'/cases/'
        if(data['ui'] == 'cui'):
            tests = []
            for n in range(1, get_num_files(path)+1):
                tests.append({
                    "i":"/mnt/tests/ip"+str(n),
                    "o":path+'op'+str(n),
                    "r":""
                })
            print(tests)
            print(path)
            # rundockers.runTest("ubuntu:16.04", path)
            return rundockers.runCUI(getdockername(data['dockLink']), tests, path)
        elif(data['ui']=='web'):
            config = {
                "host":app_config["HOST"],
                "port": data['port'],
                "host_port": ''
            }
            return rundockers.runWeb(getdockername(data['dockLink']), config)
        elif(data['ui'] == 'rest'):
            config = {
                "host": app_config["HOST"],
                "port": data['port'],
                "host_port": ''
            }

            query = 'select * from rest where assignmentId=%s'
            params =(data['assignmentId']) 
            db.execute(query,params)
            results = db.fetchall()
            col = db.description()
            rest = [dict(zip(col, row)) for row in results]
            tests = []
            for n in range(len(rest)):
                tests.append({
                    "api":rest[n]['api'],
                    "method":rest[n]['method'],
                    "status":rest[n]['statusCode'],
                    "i":"/mnt/tests/ip"+str(n+1),
                    "o":path+"/op"+str(n+1),
                    "r":""
                })
            # print(tests)
            return rundockers.runRest(getdockername(data['dockLink']), config, tests, path)
            
    return data

def getdockername(dockLink):
    parts = dockLink.split('/')
    return parts[-2]+'/'+parts[-1]

def stopDocker(container_id):
    return rundockers.stopDocker(container_id)



# runDocker(1)
# print(app_config)
# print(createAssignment("P002"))
# print(sectionFromSem("P002",3))
# print(courseFromSectionandSem("P002", 3, "A"))