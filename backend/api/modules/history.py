from ctypes import sizeof
from flask import Blueprint,request,jsonify,url_for,redirect,render_template,session
from datetime import date
import datetime
import pymysql
import yaml
import re
import traceback
import hashlib
import random
import string
import datetime
from flask_cors import CORS

#for user register

with open('config.yml', 'r') as f:
    cfg = yaml.safe_load(f)


history=Blueprint("history",__name__) 
CORS(history)


#for cut path
@history.route('/')
def index():
    return "history route"

@history.route('/checkLendClassroom',methods=['POST'])
def checkLendClassroom():
    connection = pymysql.connect(host=cfg['db']['host'],user=cfg['db']['user'],password=cfg['db']['password'],db=cfg['db']['database'])
    info = dict()
    cursor = connection.cursor()
    #ApplicationForms's PK = classroomID lendTime weekDay
    info['schoolName'] = request.values.get('schoolName')
    info['classroomID'] = request.values.get('classroomID')
    info['lendTime'] = request.values.get('lendTime')
    info['weekDay'] = request.values.get('weekDay')
    try:
        #update user state first
        insertString = 'UPDATE Users SET status = 2 WHERE schoolName=(%(schoolName)s);'
        cursor.execute(insertString, {'schoolName':info['schoolName']})
        connection.commit() #submit the data to database 
        #search the reason from ApplicationForms
        insertString = 'SELECT courseName,userName,reason from ApplicationForms WHERE classroomID=(%(classroomID)s) AND lendTime=(%(lendTime)s) AND weekDay=(%(weekDay)s);'
        cursor.execute(insertString,{'classroomID':info['classroomID'],'lendTime':info['lendTime'],'weekDay':info['weekDay']})
        rows = cursor.fetchall()
        connection.commit()
        if len(rows)==0:
            info['errors'] = 'invalid select from ApplicationForms'
        else :
            #print(rows)
            insertString = 'DELETE from ApplicationForms WHERE classroomID=(%(classroomID)s) AND lendTime=(%(lendTime)s) AND weekDay=(%(weekDay)s);'
            cursor.execute(insertString,{'classroomID':info['classroomID'],'lendTime':info['lendTime'],'weekDay':info['weekDay']})
            #rows = cursor.fetchall()
            info['lendTime'] = datetime.date.today()
            info['courseName'] = rows[0][0]
            info['userName'] = rows[0][1]
            info['reason'] = rows[0][2]
            #insert new data to history
            insertString = 'INSERT INTO History(classroomID,courseName,userName,schoolName,lendTime,returnTime,reason)values(%(classroomID)s,%(courseName)s,%(userName)s,%(schoolName)s,%(lendTime)s,NULL,%(reason)s);'
            cursor.execute(insertString,{'classroomID':info['classroomID'],'courseName':info['courseName'],'userName':info['userName'],'schoolName':info['schoolName'],'lendTime':info['lendTime'],'reason':info['reason']})
            connection.commit()
    except Exception: #get exception if there's still occured something wrong
            traceback.print_exc()
            connection.rollback()
            info['errors'] = 'checkLendClassroom fail'
    return jsonify(info)

@history.route('/returnClassroom',methods=['GET'])
def returnClassroom():
    info = dict()
    connection = pymysql.connect(host=cfg['db']['host'],user=cfg['db']['user'],password=cfg['db']['password'],db=cfg['db']['database'])
    cursor=connection.cursor()
    try:
        #select history that 'returnTime = NULL'
        insertString = 'SELECT schoolName, userName, classroomID, lendTime, returnTime, lendWeekDay, returnWeekDay, weekDay from History WHERE returnTime is NULL'
        cursor.execute(insertString)
        rows = cursor.fetchall()
        connection.commit()
        if len(rows)==0:
            info['errors'] = 'invalid select from History' 
        else :
            for i in rows:
                info['schoolName'] = rows[i][0]
                info['userName'] = rows[i][1]
                info['classroomID'] = rows[i][2]
                info['lendTime'] = rows[i][3]
                info['returnTime'] = rows[i][4]
                info['lendWeekDay'] = rows[i][5]
                info['returnWeekDay'] = rows[i][6]
                info['weekDay'] = rows[i][7]
    except Exception: #get exception if there's still occured something wrong
            traceback.print_exc()
            connection.rollback()
            info['errors'] = 'returnClassroom fail'
    return jsonify(info)


#get all data from history
@history.route('/seeClassroomHistory',methods=['GET'])
def seeClassroomHistory():
    info = dict()
    errors = []
    connection = pymysql.connect(host=cfg['db']['host'],user=cfg['db']['user'],password=cfg['db']['password'],db=cfg['db']['database'])
    cursor=connection.cursor()
    #undo: displayed data <= 100 
    cursor.execute("SELECT * from History ")
    rows = cursor.fetchall()
    connection.commit()
    if len(rows) == 0:
        errors.append("No history exist!")
    else:
        info['history'] = []
        for row in rows:
            tmp = []
            for i in range(7):
                print(type(row[i]))
                if (i == 4 or i == 5) and row[i] != None:
                    tmp.append(row[i].strftime('%Y/%m/%d %H:%M:%S'))
                else :
                    tmp.append(row[i])
            info['history'].append(tmp)
    info['errors'] = errors
    return jsonify(info)

#   email confirm undo
#   if a user input an error email (but legal), his student's ID fucked up. 

#   html should alert if sign up failed when reload