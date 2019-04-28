from flask import Flask, flash,session, render_template, request, redirect, Response ,jsonify, json, url_for, send_file
from string import Template
import utilities


app = Flask(__name__)
app.secret_key = 'droplet'

#To display the home page

@app.route('/profile')
@app.route('/')
def index():
    if 's_id' in session:
        return render_template('stu_profile.html', name = session["name"])
    elif 'p_id' in session:
        return render_template('prof_profile.html', name = session["name"])
    else:
        return render_template("index.html")

#To validate user form data
@app.route('/validate',methods=['POST'])
def validate():
    data = json.loads(request.data)
    results = utilities.validate(data)
    if results:
        row = results[0]

        if(row[3] == data["password"]):
            # do session stuff
            session.clear()
            if(data["role"] == "student"):
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

@app.route('/getmanual')
def getmanual():
    if 's_id' in session:
        return send_file('../manuals/Student.zip', as_attachment=True, cache_timeout=1) 
    elif 'p_id' in session:
        return send_file('../manuals/Professor.pdf', as_attachment=True, cache_timeout=1)
    else:
        return redirect(url_for('index'))


#To logout
@app.route('/logout')
def logout():
    if 's_id' in session:
        session.pop('s_id')    
    elif 'p_id' in session:
        session.pop('p_id')
    return redirect(url_for('index'))

#####
# Common Pages
#####

#To display profile page



@app.route('/get/assignments')
def getAssignments():
    if 'p_id' in session:
        return json.dumps(utilities.getAssignments(session["p_id"],"prof"))
    elif 's_id' in session:
        return json.dumps(utilities.getAssignments(session["s_id"],"stu"))
    else:
        return redirect(url_for('index'))


@app.route('/get/<assignment_id>')
def getAssignment(assignment_id):
    if 'p_id' in session:
        data = utilities.getAssignment(assignment_id)
        return render_template('prof_assignment.html', name = session["name"], **data)
    elif 's_id' in session:
        data = utilities.getAssignment(assignment_id)
        return render_template('stu_submission.html', name = session["name"], **data)
    else:
        return redirect(url_for('index'))

@app.route('/get/web/<assignment_id>')
def getWeb(assignment_id):
    if 'p_id' in session or 's_id' in session:
        return json.dumps(utilities.getWeb(assignment_id))
    else:
        return redirect(url_for('index'))


@app.route('/get/rest/<assignment_id>')
def getRest(assignment_id):
    if 'p_id' in session or 's_id' in session:
        return json.dumps(utilities.getRest(assignment_id))
    else:
        return redirect(url_for('index'))

@app.route('/get/cui/<assignment_id>')
def getCui(assignment_id):
    if 'p_id' in session or 's_id' in session:
        return json.dumps(utilities.getCui(assignment_id))
    else:
        return redirect(url_for('index'))

@app.route('/get/<assignment_id>/submission')
def getSubmission(assignment_id):
    if 'p_id' in session:
        data = utilities.getSubmission(assignment_id)
        return render_template('prof_submission.html', name = session["name"], **data)
    elif 's_id' in session:
        return json.dumps(utilities.getSubmission(assignment_id))
    else:
        return redirect(url_for('index'))

@app.route('/<assignment_id>/cases', methods=['GET','POST'])
def getCases(assignment_id):
    if 'p_id' in session or 's_id' in session:
        return send_file('../tests/'+str(assignment_id)+'/cases.zip', attachment_filename='cases.zip')
    else:
        return redirect(url_for('index'))

@app.route('/result/<assignment_id>/<file>', methods=['GET','POST'])
def getResult(assignment_id, file):
    if 'p_id' in session or 's_id' in session:
        return send_file('../tests/'+str(assignment_id)+'/result/'+file, attachment_filename=file)
    else:
        return redirect(url_for('index'))

@app.route('/run/<submission_id>/')
def runDocker(submission_id):
    if 'p_id' in session or 's_id' in session:
        return json.dumps(utilities.runDocker(submission_id)) 
    else:
        return redirect(url_for('index'))

@app.route('/stop/<container_id>/')
def stopDocker(container_id):
    if 'p_id' in session or 's_id' in session:
        return json.dumps(utilities.stopDocker(container_id)) 
    else:
        return redirect(url_for('index'))


#####
# Prof Pages
#####

@app.route('/professor/create/assignment')
def createAssigment():
    if 'p_id' in session:
        data = utilities.createAssignment(session['p_id'])
        return render_template('prof_create.html', name = session["name"], semesters = data)
    else:
        return redirect(url_for('index'))

@app.route('/professor/get/<semester>/sections')
def sectionFromSem(semester):
    if 'p_id' in session:
        data = utilities.sectionFromSem(session['p_id'], semester)
        return json.dumps(data)
    else:
        return redirect(url_for('index'))

@app.route('/professor/get/<semester>/<section>/courses')
def courseFromSectionandSem(semester, section):
    if 'p_id' in session:
        data = utilities.courseFromSectionandSem(session['p_id'], semester, section)
        return json.dumps(data)
    else:
        return redirect(url_for('index'))

@app.route('/professor/create/assignment/confirm',methods=['GET','POST'])
def createAssignmentConfirm():
    if 'p_id' in session:
        result = utilities.createAssignmentConfirm(request.form, request.files, session['p_id'])
        if(result=="Success"):
            return redirect(url_for('profile'))
        else:
            return result
    else:
        return redirect(url_for('index'))

@app.route('/professor/get/<assignment_id>')
def getSubmissions(assignment_id):
    if 'p_id' in session:
        data = utilities.getSubmissions(assignment_id)
        return json.dumps(data)
    else:
        return redirect(url_for('index'))

####
# Student Functions
####

@app.route('/student/create/<assignment_id>/submission')
def createSubmission(assignment_id):
    if 's_id' in session:
        ui = utilities.getUI(assignment_id)
        return render_template('stu_submit.html', name = session["name"], ui = ui, assignmentId = assignment_id)
    else:
        return redirect(url_for('index'))

@app.route('/student/create/<assignment_id>/submission/confirm/<ui>',methods=["GET","POST"])
def createSubmissionConfirm(assignment_id, ui):
    if 's_id' in session:
        result = utilities.createSubmissionConfirm(assignment_id, ui, request.form, request.files, session['s_id'])
        if(result=="Success"):
            return redirect(url_for('profile'))
        else:
            return result
    else:
        return redirect(url_for('index'))

@app.route('/student/create/dockerfile')
def createDockerfile():
    if 's_id' in session:
        return render_template('stu_dockerfile.html', name = session["name"])
    else:
        return redirect(url_for('index'))




if __name__ == '__main__':
# run!
    app.run(host="0.0.0.0",port=5000, debug=True)








