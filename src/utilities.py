import os, os.path
import glob
from database import *
import datetime
from shutil import make_archive
import rundockers
import json
from werkzeug.utils import secure_filename
import pathlib

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
            query = 'select assignmentId, title, semester, section, courseName, submission from teaches, assignment, course where assignment.teachesId=teaches.teachesId and teaches.courseId=course.courseId and teaches.userId=%s order by submission desc'
        else:
            query = 'select assignment.assignmentId, title, semester, takes.section, courseName, submission from assignment, teaches, takes, course where assignment.teachesId=teaches.teachesId and teaches.courseid=takes.courseid and teaches.section=takes.section and course.courseId=takes.courseId and takes.userId=%s order by submission desc'
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
        query = 'select assignment.assignmentId, ui, submissionId, gitLink, dockLink, docLink, ui, takes.userId from submission,assignment,takes where assignment.assignmentId=%s and submission.assignmentId=assignment.assignmentId and submission.takesId=takes.takesId;'
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
def createAssignmentConfirm(form, files, pid):
    with Database() as db:
        query = 'select teachesId from course,teaches where semester=%s and section=%s and courseName=%s and teaches.userId=%s and course.courseId=teaches.courseId;'
        params = ([form['semester'], form['section'], form['course'], pid])
        db.execute(query,params)
        results = db.fetchone()
        print(results)
        print(form['submission'])
        query = 'insert into assignment(title,descr,db,ui,submission,teachesId) values (%s,%s,%s,%s,%s,%s)'
        params =([form['title'],form['descr'],form['database'],form['uitype'],form['submission'],results[0]])
        db.execute(query,params)
        result = db.fetchall()
        print(result)
        query = 'select assignmentId from assignment where title=%s and descr=%s and db=%s and ui=%s and submission =%s and teachesId=%s'
        params =([form['title'],form['descr'],form['database'],form['uitype'],form['submission'],results[0]])
        db.execute(query,params)
        results = db.fetchone()
        assignmentId = results[0]
        if(form['uitype']=='web'):
            tests = getWebTests(form, files)
            for i in range(len(tests)):
                query = 'insert into web values(%s, %s, %s)'
                params = ([i+1, tests[i]["scenario"], assignmentId])
                db.execute(query,params)
                results = db.fetchone()
        elif(form['uitype']=='rest'):
            tests = getRestTests(form, files)
            for i in range(len(tests)):
                query = 'insert into rest values(%s, %s, %s, %s, %s)'
                params = ([i+1, tests[i]["api"], tests[i]["method"], tests[i]["status_code"], assignmentId])
                db.execute(query,params)
                results = db.fetchone()
            uploadFiles(tests, assignmentId)
        elif(form['uitype']=='cui'):
            tests = getCUITests(form, files)
            query = 'insert into cui values(%s, %s)'
            params = ([form["exec_name"], results[0]])
            db.execute(query,params)
            results = db.fetchone()
            uploadFiles(tests, assignmentId)
        return "Success"

# Get ui for submitting assignment
def getUI(assignment_id):
    with Database() as db:
        query = 'select ui from assignment where assignmentId=%s'
        params = ([assignment_id])
        db.execute(query,params)
        results = db.fetchone()
    return results[0]

# Create a submission
def createSubmissionConfirm(assignment_id, ui, form, files, sid):
    path = app_config["APP_ROOT"]+'tests/'+str(assignment_id)+'/result/'
    pathlib.Path(path).mkdir(parents=True, exist_ok=True)
    with Database() as db:
        query = 'select takesId from teaches, takes, assignment where teaches.courseid=takes.courseid and teaches.section=takes.section and teaches.teachesId=assignment.teachesId and assignmentId=%s;'
        params = ([assignment_id])
        db.execute(query,params)
        results = db.fetchone()
        query = 'insert into submission(gitlink,docklink,doclink,port,takesid,assignmentid) values (%s,%s,%s,%s,%s,%s);'
        if(ui == 'web'):
            params =([form['gitlink'],form['docklink'],form['doclink'],form['web-port'],results[0],assignment_id])
            files["selenium"].save(os.path.join(path,secure_filename("selenium.side")))
        elif(ui == 'rest'):
            params =([form['gitlink'],form['docklink'],form['doclink'],form['api-port'],results[0],assignment_id])
            files["postman"].save(os.path.join(path,secure_filename("postman.json")))
            make_archive("postman", 'zip', path+"postman.json")
        elif(ui == 'cui'):
            params =([form['gitlink'],form['docklink'],form['doclink'],0,results[0],assignment_id])
        db.execute(query,params)
        return "Success"

# File related Utilities
def get_num_files(path):
    return len(glob.glob1(path,"ip*"))

def uploadFiles(tests, assignmentId):
    path = app_config["APP_ROOT"]+'tests/'+str(assignmentId)+'/cases/'
    pathlib.Path(path).mkdir(parents=True, exist_ok=True)
    for i in range(len(tests)):
        tests[i]["input"].save(os.path.join(path,secure_filename("ip"+str(i+1))))
        tests[i]["output"].save(os.path.join(path,secure_filename("op"+str(i+1))))
    zipfiles("cases",path)
    return "Success"

def zipfiles(zipname, path):
    return make_archive(zipname, 'zip', path)

#Docker related utilities
def runDocker(submission_id):
    with Database() as db:
        query = 'select assignment.assignmentId, submissionId, port, ui, dockLink, takes.userId from submission, assignment,takes where submissionId=%s and submission.assignmentId=assignment.assignmentId and submission.takesId=takes.takesId;'
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
                    "o":path+"op"+str(n+1),
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


# Miscellaneouss Utilities
def getWebTests(form, files):
    tests = [{"scenario":v} for k,v in form.items() if 'scenario' in k]
    return tests

def getRestTests(form, files):
    tests = []
    # print(form)
    apis = [{k[-1]:v} for k,v in form.items() if 'api' in k]
    methods = [{k[-1]:v} for k,v in form.items() if 'method' in k]
    stats = [{k[-1]:v} for k,v in form.items() if 'status_code' in k]
    inputs = [{k[-1]:v} for k,v in files.items() if 'input' in k]
    outputs = [{k[-1]:v} for k,v in files.items() if 'output' in k]
    for i in range(len(apis)):
        test = {}
        test["api"] = apis[i][str(i+1)]
        test["method"] = methods[i][str(i+1)]
        test["status_code"] = stats[i][str(i+1)]
        test["input"] = inputs[i][str(i+1)]
        test["output"] = outputs[i][str(i+1)]
        tests.append(test)
    print(tests)
    return tests

def getCUITests(form, files):
    tests = []
    inputs = [{k[-1]:v} for k,v in files.items() if 'input' in k]
    outputs = [{k[-1]:v} for k,v in files.items() if 'output' in k]
    for i in range(len(inputs)):
        test = {}
        test["input"] = inputs[i][str(i+1)]
        test["output"] = outputs[i][str(i+1)]
        tests.append(test)
    return tests


# runDocker(1)
# print(app_config)
# print(createAssignment("P002"))
# print(sectionFromSem("P002",3))
# print(courseFromSectionandSem("P002", 3, "A"))
# print(zipfiles(app_config["APP_ROOT"]+'tests/'+str(2)+'/cases', app_config["APP_ROOT"]+'tests/'+str(2)+'/cases'))