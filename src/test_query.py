from database import *

                # <th>Assignment</th>
                # <th>Semester</th>
                # <th>Section</th>
                # <th>Subject</th>
                # <th>Submission Date</th>

with Database() as db:
    # need user, assignment, teaches, course, section
    query = 'select assignmentId, title, semester, section, courseName , descr, db, ui, submission from assignment, teaches, course where assignmentId="1" and assignment.teachesId=teaches.teachesId and teaches.courseId=course.courseId;'
    params =(["P002"])
    db.execute(query,params)
    results = db.fetchall()
    col = db.description()
    data = [dict(zip(col, row)) for row in results]
print(results)