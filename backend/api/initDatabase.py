
import yaml
import mysql.connector as mariadb
import pymysql


with open('config.yml', 'r') as f:
    cfg = yaml.safe_load(f)

connection = mariadb.connect(host=cfg['db']['host'],user=cfg['db']['user'],password=cfg['db']['password'],db=cfg['db']['database'],charset='utf8')

cursor = connection.cursor()
cursor.execute("DROP TABLE IF EXISTS Users;")
connection.commit()

cursor.execute("DROP TABLE IF EXISTS Classrooms;")
connection.commit()

cursor.execute("DROP TABLE IF EXISTS Scheduler;")
connection.commit()

cursor.execute("DROP TABLE IF EXISTS ApplicationForms;")
connection.commit()

cursor.execute("DROP TABLE IF EXISTS Historys;")
connection.commit()

cursor.execute("CREATE TABLE IF NOT EXISTS Users( \
    userName varchar(30) NOT NULL,\
    schoolName varchar(10) NOT NULL,\
    password varchar(50) NOT NULL,\
    phoneNumber varchar(10) NOT NULL,\
    Email varchar(40) NOT NULL, \
    isAdmin int NOT NULL,\
    identityCode varchar(6),\
    status int NOT NULL,\
    apply int,\
    PRIMARY KEY (schoolName) );")
connection.commit()

cursor.execute("CREATE TABLE IF NOT EXISTS Classrooms( \
    classroomID  varchar(10) NOT NULL,\
    status int NOT NULL,\
    computer boolean NOT NULL,\
    projector boolean NOT NULL,\
    blackboard boolean NOT NULL,\
    whiteboard boolean NOT NULL,\
    equipment1 varchar(15) NULL,\
    equipment2 varchar(15) NULL,\
    equipment3 varchar(15) NULL,\
    equipment4 varchar(15) NULL,\
    equipment5 varchar(15) NULL,\
    PRIMARY KEY (classroomID) );")
connection.commit()

cursor.execute("CREATE TABLE IF NOT EXISTS Scheduler( \
    classroomID  varchar(10) NOT NULL,\
    courseName varchar(20) NOT NULL,\
    lendTime int NOT NULL,\
    returnTime int NOT NULL,\
    weekDay int NOT NULL,\
    PRIMARY KEY (classroomID,lendTime,weekday) );")
connection.commit()

cursor.execute("CREATE TABLE IF NOT EXISTS ApplicationForms( \
    classroomID  varchar(10) NOT NULL,\
    courseName varchar(20) NOT NULL,\
    userName varchar(30) NOT NULL,\
    schoolName varchar(10) NOT NULL,\
    phoneNumber varchar(10) NOT NULL,\
    lendTime int NOT NULL,\
    returnTime int NOT NULL,\
    weekDay int NOT NULL,\
    reason varchar(250) NOT NULL,\
    PRIMARY KEY (classroomID,lendTime,weekday) );")
connection.commit()

cursor.execute("CREATE TABLE IF NOT EXISTS History( \
    classroomID  varchar(10) NOT NULL,\
    courseName varchar(20) NOT NULL,\
    userName varchar(30) NOT NULL,\
    schoolName varchar(10) NOT NULL,\
    lendTime datetime NOT NULL,\
    returnTime datetime ,\
    reason varchar(250) NOT NULL,\
    PRIMARY KEY (classroomID,lendTime) );")
connection.commit()