insert into user values ("S001","Billy","billy@gmail.com","billy","student");
insert into user values("S002","Cooper","copper@gmail.com","cooper","student");
insert into user values("S003","Harold","harold@gmail.com","harold","student");
insert into user values("P001","Rick","rick@gmail.com","rick","prof");
insert into user values("P002","Fred","fred@gmail.com","fred","prof");
insert into user values("S004", "Lina" , "Lina@gmail.com" , "Lina" , "student");
insert into user values("P003", "Ursa" , "Ursa@gmail.com" , "Ursa" , "prof");
insert into user values("S005", "Kunkka" , "Kunkka@gmail.com" , "Kunkka" , "student");
insert into user values("S006", "Abaddon" , "Abaddon@gmail.com" , "Abaddon" , "student");
insert into user values("S007", "Axe" , "Axe@gmail.com" , "Axe" , "student");
insert into user values("S008", "Bane" , "Bane@gmail.com" , "Bane" , "student");
insert into user values("S009", "Clark" , "Clark@gmail.com" , "Clark" , "student");
insert into user values("S010", "Lich" , "Lich@gmail.com" , "Lich" , "student");
insert into user values("P004", "Mirana" , "Mirana@gmail.com" , "Mirana" , "student");
insert into course values("C001","Databases",4);
insert into course values("C002","Algorithms",3);
insert into course values("C003","Web Tech II",7);
insert into course values("C004","Data Science",7);
insert into takes(section, userId, courseId) values('A' , "S001", "C001");
insert into takes(section, userId, courseId) values('A' , "S002", "C002");
insert into takes(section, userId, courseId) values('A' , "S003", "C003");
insert into takes(section, userId, courseId) values('A' , "S004", "C004");
insert into takes(section, userId, courseId) values('A' , "S005", "C001");
insert into takes(section, userId, courseId) values('B' , "S006", "C002");
insert into takes(section, userId, courseId) values('B' , "S001", "C003");
insert into takes(section, userId, courseId) values('B' , "S002", "C004");
insert into takes(section, userId, courseId) values('B' , "S003", "C001");
insert into takes(section, userId, courseId) values('B' , "S004", "C002");
insert into takes(section, userId, courseId) values('B' , "S005", "C003");
insert into teaches(section, userId, courseId) values('A' , "P001", "C001");
insert into teaches(section, userId, courseId) values('A' , "P002", "C002");
insert into teaches(section, userId, courseId) values('A' , "P003", "C003");
insert into teaches(section, userId, courseId) values('A' , "P004", "C004");
insert into teaches(section, userId, courseId) values('B' , "P001", "C004");
insert into teaches(section, userId, courseId) values('B' , "P002", "C003");
insert into teaches(section, userId, courseId) values('B' , "P003", "C002");
insert into teaches(section, userId, courseId) values('B' , "P004", "C001");
insert into assignment(title,descr,db,ui,submission,teachesId) values ("Mergesort","Test MergeSort Algo",'none','cui',"2019-04-04",2);
insert into cui values("merge", 1);
insert into assignment(title,descr,db,ui,submission,teachesId) values ("Rest APIs", "Build a rest api for a simple todo list", 'none','rest',"2019-04-04",6);
insert into rest values(1, "/tasks","GET",200,2);
insert into rest values(2, "/tasks/1","GET",200,2);
insert into assignment(title,descr,db,ui,submission,teachesId) values ("Panda-Flask", "Render panda charts using Python-Flask", 'none','web',"2019-04-04",4);
insert into web values(1, "Render pandas DataFrame wholesale", 3);
insert into web values(2, "Render pandas DataFrame row by row+", 3);
insert into web values(3, "Display an embedded Bokeh chart", 3);
insert into submission(gitlink, docklink, docLink, port, takesId, assignmentId) values("http://github.com/kaveri-s","https://hub.docker.com/rubyphoenix/cui-sample","www.google.com",0, 2, 1);
insert into submission(gitlink, docklink, docLink, port, takesId, assignmentId) values("http://github.com/kaveri-s", "https://hub.docker.com/rubyphoenix/rest-sample", "www.google.com",5000, 7, 2);
insert into submission(gitlink, docklink, docLink, port, takesId, assignmentId) values("http://github.com/kaveri-s","https://hub.docker.com/rubyphoenix/web-sample", "www.google.com", 5957, 4, 3);