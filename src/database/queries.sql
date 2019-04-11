select * from user where userId=%s and email=%s and pass=%s and userrole=%s

-- get semesters, section, courses
select teachesId, semester, section, courseName from user, teaches, course
    where teaches.userId=user.userId and teaches.courseId = course.courseId
    and user.userId="P002";

-- create the assignment using teachesId thus obtained
insert into assignment(title,descr,db,ui,submission,teachesId) values ("algo","just a test","none","cli","2019-04-04","2");

-- show assignment on main page
select assignmentId, title, semester, section, courseName, submission 
    from user, teaches, assignment, course
    where assignment.teachesId=teaches.teachesId and teaches.userId=user.userId and teaches.courseId=course.courseId
    and user.userId="P002";

-- show an assignment's details
select assignmentId, title, semester, section, courseName , descr, db, ui, submission from assignment, teaches, course where assignmentId="1" and assignment.teachesId=teaches.teachesId and teaches.courseId=course.courseId;

-- get submissions of an assignment
    select * from submission,takes where submission.assignmentId="ASS" and submission.takesId=takes.takesId; 
-- get submission details
    select * from submission where assignmentId="ASS" and takesId; 

-- get assignment list for student
    select * from submission,takes where and submission.takesId=takes.takesId and takes.userId="Billy";
-- get takesId of student from details
    select takesId from submission  where submission.submissionId= "2";
-- insert submission

-- see submission details if submitted
