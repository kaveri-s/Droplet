from flask import Flask, flash,session, render_template, request, redirect, Response ,jsonify, json, url_for
from database import *

app = Flask(__name__)
app.secret_key = 'droplet'

@app.route('/professor/get/assignments')
def getAssignments():
    if 'p_id' in session:
        pid = session["p_id"]
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

if __name__ == '__main__':
# run!
    app.run(debug=True)