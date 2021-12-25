
DROP TABLE IF EXISTS Users;
DROP TABLE IF EXISTS Classrooms;
DROP TABLE IF EXISTS Scheduler;
DROP TABLE IF EXISTS ApplicationForms;
DROP TABLE IF EXISTS Historys;

CREATE TABLE IF NOT EXISTS Users( \
    userName varchar(30) NOT NULL,\
    schoolName varchar(10) NOT NULL,\
    password varchar(50) NOT NULL,\
    phoneNumber varchar(10) NOT NULL,\
    Email varchar(40) NOT NULL, \
    isAdmin int NOT NULL,\
    identityCode varchar(6),\
    status int NOT NULL,\
    apply int,\
    PRIMARY KEY (schoolName) );

CREATE TABLE IF NOT EXISTS Classrooms( \
    classroomID  varchar(10) NOT NULL,\
    status int NOT NULL,\
    equipment1 varchar(15) NULL,\
    equipment2 varchar(15) NULL,\
    equipment3 varchar(15) NULL,\
    equipment4 varchar(15) NULL,\
    equipment5 varchar(15) NULL,\
    PRIMARY KEY (classroomID) );

CREATE TABLE IF NOT EXISTS Scheduler( \
    classroomID  varchar(10) NOT NULL,\
    courseName varchar(20) NOT NULL,\
    lendTime int NOT NULL,\
    returnTime int NOT NULL,\
    weekDay int NOT NULL,\
    PRIMARY KEY (classroomID,lendTime,weekday) );

CREATE TABLE IF NOT EXISTS ApplicationForms( \
    classroomID  varchar(10) NOT NULL,\
    courseName varchar(20) NOT NULL,\
    userName varchar(30) NOT NULL,\
    schoolName varchar(10) NOT NULL,\
    phoneNumber varchar(10) NOT NULL,\
    lendTime int NOT NULL,\
    returnTime int NOT NULL,\
    weekDay int NOT NULL,\
    reason varchar(250) NOT NULL,\
    PRIMARY KEY (classroomID,lendTime,weekday) );

CREATE TABLE IF NOT EXISTS Historys( \
    classroomID  varchar(10) NOT NULL,\
    courseName varchar(20) NOT NULL,\
    userName varchar(30) NOT NULL,\
    schoolName varchar(10) NOT NULL,\
    lendTime datetime NOT NULL,\
    returnTime datetime NOT NULL,\
    reason varchar(250) NOT NULL,\
    PRIMARY KEY (classroomID,lendTime) );