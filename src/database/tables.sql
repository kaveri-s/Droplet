drop table submission;
drop table cli;
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
    userrole ENUM('prof', 'student')
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
    descr varchar(30), 
    db enum('prof','stu','none'),
    ui enum('web', 'rest', 'cli'),
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
    assignmentId int, 
    FOREIGN KEY (assignmentId) REFERENCES assignment(assignmentId)
);

CREATE TABLE cli(
    execName varchar(50), 
    params varchar(50), 
    assignmentId int, 
    FOREIGN KEY(assignmentId) REFERENCES assignment(assignmentId)
);

CREATE TABLE submission(
    gitLink varchar(50),
    docLink varchar(50),
    toolPath varchar(50), 
    reportLink varchar(50),
    host varchar(50),
    port int, 
    takesId int,
    assignmentId int,
    FOREIGN KEY (takesId) REFERENCES takes(takesId),
    FOREIGN KEY (assignmentId) REFERENCES assignment(assignmentId)
);
