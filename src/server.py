from flask import Flask, flash,session, render_template, request, redirect, Response ,jsonify, json, url_for, send_file
from string import Template
import utilities


app = Flask(__name__)
app.secret_key = 'droplet'

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
# Common Pages
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

@app.route('/get/assignments')
def getAssignments():
    if 'p_id' in session:
        return json.dumps(utilities.getAssignments(session["p_id"],"prof"))
    elif 's_id' in session:
        return json.dumps(utilities.getAssignments(session["s_id"],"stu"))
    else:
        return render_template('index.html')


@app.route('/get/<assignment_id>')
def getAssignment(assignment_id):
    if 'p_id' in session:
        data = utilities.getAssignment(assignment_id)
        return render_template('prof_assignment.html', name = session["name"], **data)
    elif 's_id' in session:
        data = utilities.getAssignment(assignment_id)
        return render_template('stu_submission.html', name = session["name"], **data)
    else:
        return render_template('index.html')

@app.route('/get/web/<assignment_id>')
def getWeb(assignment_id):
    if 'p_id' in session or 's_id' in session:
        return json.dumps(utilities.getWeb(assignment_id))
    else:
        return render_template('index.html')


@app.route('/get/rest/<assignment_id>')
def getRest(assignment_id):
    if 'p_id' in session or 's_id' in session:
        return json.dumps(utilities.getRest(assignment_id))
    else:
        return render_template('index.html')

@app.route('/get/cui/<assignment_id>')
def getCui(assignment_id):
    if 'p_id' in session or 's_id' in session:
        return json.dumps(utilities.getCui(assignment_id))
    else:
        return render_template('index.html')

@app.route('/get/<assignment_id>/submission')
def getSubmission(assignment_id):
    if 'p_id' in session:
        data = utilities.getSubmission(assignment_id)
        return render_template('prof_submission.html', name = session["name"], **data)
    elif 's_id' in session:
        return json.dumps(utilities.getSubmission(assignment_id))
    else:
        return render_template('index.html')

@app.route('/cases/<assignment_id>', methods=['GET','POST'])
def getCases(assignment_id):
    return send_file('../tests/'+str(assignment_id)+'/cases.zip', attachment_filename='cases.zip')

@app.route('/run/<submission_id>/')
def runDocker(submission_id):
    if 'p_id' in session or 's_id' in session:
        return json.dumps(utilities.runDocker(submission_id)) 
    else:
        return render_template('index.html')

#####
# Prof Pages
#####

@app.route('/professor/create/assignment')
def createAssigment():
    if 'p_id' in session:
        return render_template('prof_create.html', name = session["name"])
    else:
        return render_template('index.html')

@app.route('/professor/create/assignment/confirm',methods=['POST'])
def createAssignmentConfirm():
    if 'p_id' in session:
        return utilities.createAssignmentConfirm(json.loads(request.data), session['p_id'])
    else:
        return render_template('index.html')

@app.route('/professor/get/<assignment_id>')
def getSubmissions(assignment_id):
    if 'p_id' in session:
        data = utilities.getSubmissions(assignment_id)
        return json.dumps(data)
    else:
        return render_template('index.html')

####
# Student Functions
####

@app.route('/student/create/submission')
def createSubmission():
    if 's_id' in session:
        return render_template('stu_submit.html', name = session["name"])
    else:
        return render_template('index.html')

@app.route('/student/create/submission/confirm',methods=["POST"])
def createSubmissionConfirm():
    if 's_id' in session:
        return utilities.createSubmissionConfirm(json.loads(request.data), session['s_id'])
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








