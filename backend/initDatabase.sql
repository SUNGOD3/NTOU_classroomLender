
DROP TABLE IF EXISTS Users;
DROP TABLE IF EXISTS Classrooms;
DROP TABLE IF EXISTS Scheduler;
DROP TABLE IF EXISTS ApplicationForms;

CREATE TABLE IF NOT EXISTS Users( 
    userName varchar(30) NOT NULL,
    schoolName varchar(10) NOT NULL,
    password varchar(50) NOT NULL,
    Email varchar(40) NOT NULL,
    isAdmin int NOT NULL,
    identityCode varchar(6),
    accessKey varchar(100),
    status int NOT NULL,
    PRIMARY KEY (schoolName) );

CREATE TABLE IF NOT EXISTS Classrooms( 
   classroomID varchar(10) NOT NULL,
    department varchar(15) NOT NULL,
    status int NOT NULL,
    equipment1 varchar(15) NOT NULL,
    equipment2 varchar(15) NOT NULL,
    equipment3 varchar(15) NOT NULL,
    equipment4 varchar(15) NOT NULL,
    equipment5 varchar(15) NOT NULL,
    PRIMARY KEY (classroomID) );

CREATE TABLE IF NOT EXISTS Scheduler( \
    classroomID  varchar(10) NOT NULL,
    department varchar(15) NOT NULL,
    courseName varchar(20) NOT NULL,
    time int NOT NULL,
    weekDay int NOT NULL,
    PRIMARY KEY (classroomID) );

CREATE TABLE IF NOT EXISTS ApplicationForms( \
    classroomID  varchar(10) NOT NULL,\
    department varchar(15) NOT NULL,\
    courseName varchar(20) NOT NULL,\
    userName varchar(30) NOT NULL,\
    schoolName varchar(10) NOT NULL,\
    Email varchar(40) NOT NULL, \
    time int NOT NULL,\
    weekDay int NOT NULL,\
    reason varchar(250) NOT NULL,\
    PRIMARY KEY (classroomID) );
