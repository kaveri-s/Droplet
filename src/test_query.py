from database import *

                # <th>Assignment</th>
                # <th>Semester</th>
                # <th>Section</th>
                # <th>Subject</th>
                # <th>Submission Date</th>

with Database() as db:
    # need user, assignment, teaches, course, section
    query = 'select assignmentId, title, semester, teaches.section, courseName, submission from user, teaches, assignment, course where assignment.teachesId=teaches.teachesId and teaches.userId=user.userId and teaches.courseId=course.courseId and user.userId=%s order by submission desc'
    params =(["P002"])
    db.execute(query,params)
    results = db.fetchall()
    col = db.description()
    data = [dict(zip(col, row)) for row in results]
print(results)