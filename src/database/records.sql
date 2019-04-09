insert into user values ("S001","Billy","billygreen@gmail.com","billy","student");
insert into user values("S002","Cooper","copperkumar@gmail.com","cooper","student");
insert into user values("S003","Harold","haroldlebron@gmail.com","harold","student");
insert into user values("P001","Rick","rickmorty@gmail.com","rick","prof");
insert into user values("P002","Fred","fredflinstone@gmail.com","fred","prof");
insert into course values("C001","Databases",2018);
insert into course values("C002","Algorithms",2018);
insert into course values("C003","Web Tech II",2018);
insert into takes(section, userId, courseId) values('C' , "S001", "C001");
insert into takes(section, userId, courseId) values('C' , "S002", "C002");
insert into takes(section, userId, courseId) values('C' , "S003", "C003");
insert into teaches(userId, courseId) values("P001", "C001");
insert into teaches(userId, courseId) values("P002", "C002");
insert into teaches(userId, courseId) values("P002", "C003");

