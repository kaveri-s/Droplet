drop table submission;
drop table cui;
drop table rest;
drop table web;
drop table assignment;
drop table teaches;
drop table takes;
drop table course;
drop table user;


CREATE TABLE user (
    userId VARCHAR(20) NOT NULL primary key,
    username VARCHAR(40), 
    email VARCHAR(40), 
    pass VARCHAR(20) NOT NULL,
    userrole ENUM ('prof', 'student')
);

CREATE TABLE course( 
    courseId varchar(20) primary key not null, 
    courseName VARCHAR(40), 
    semester int
);

CREATE TABLE takes( 
    takesId int AUTO_INCREMENT primary key,
    section char(1), 
    userId varchar(20) not null, 
    courseId varchar(20) not null, 
    FOREIGN KEY (userId) REFERENCES user(userId),
    FOREIGN KEY (courseId) REFERENCES course(courseId)
);

CREATE TABLE teaches(
    teachesId int  AUTO_INCREMENT primary key, 
    courseId varchar(20) not null, 
    userId varchar(20) not null,
    section varchar(20) not null, 
    FOREIGN KEY (userId) REFERENCES user(userId),
    FOREIGN KEY (courseId) REFERENCES course(courseId)
);

CREATE TABLE assignment(
    assignmentId int AUTO_INCREMENT primary key, 
    title varchar(30) not null, 
    descr text, 
    db enum('yes','none'),
    ui enum('web', 'rest', 'cui'),
    submission date,
    teachesId int,
    FOREIGN KEY (teachesId) REFERENCES teaches(teachesId)
);

CREATE TABLE web(
    testno int,
    scenario varchar(100), 
    assignmentId int, 
    FOREIGN KEY (assignmentId) REFERENCES assignment(assignmentId)
);

CREATE TABLE rest(
    testno int,
    api varchar(50),
    method varchar (10),
    statusCode int,
    assignmentId int, 
    FOREIGN KEY (assignmentId) REFERENCES assignment(assignmentId)
);

CREATE TABLE cui(
    execName varchar(50), 
    assignmentId int, 
    FOREIGN KEY(assignmentId) REFERENCES assignment(assignmentId)
);

CREATE TABLE submission(
    submissionId int not null primary key AUTO_INCREMENT,
    gitLink varchar(100),
    dockLink varchar(100),
    docLink varchar(100),
    port int, 
    takesId int,
    assignmentId int,
    FOREIGN KEY (takesId) REFERENCES takes(takesId),
    FOREIGN KEY (assignmentId) REFERENCES assignment(assignmentId)
);
