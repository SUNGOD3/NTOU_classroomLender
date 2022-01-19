from flask import Blueprint,request,jsonify,session
import pymysql
import yaml
import re
import traceback
import hashlib
import random
import string
import datetime
from datetime import timedelta
from flask_cors import CORS

with open('config.yml', 'r') as f:
    cfg = yaml.safe_load(f)
    
ApplicationForms=Blueprint("ApplicationForms",__name__) 
CORS(ApplicationForms,resources={r"/*": {"origins": "*"}},supports_credentials=True)

#for cut path
@ApplicationForms.route('/')
def index():
    return "ApplicationForms route"

@ApplicationForms.route('/getApplicationForms',methods=['GET'])
def getApplicationForms():
    info = dict()
    errors = []
    connection = pymysql.connect(host=cfg['db']['host'],user=cfg['db']['user'],password=cfg['db']['password'],db=cfg['db']['database'])
    cursor=connection.cursor()
    cursor.execute("SELECT schoolName,userName,classroomID,lendTime,returnTime,weekDay,reason from ApplicationForms")
    rows = cursor.fetchall()
    connection.commit()
    if len(rows) == 0:
        errors.append("No ApplicationForms exist!")
    else:
        info['data'] = []
        for row in rows:
            info['data'].append(""+row[0]+","+row[1]+","+row[2]+","+str(row[3])+","+str(row[4])+','+str(row[5])+','+str(row[6]))
    info['errors'] = errors
    return jsonify(info)

@ApplicationForms.route('/lendClassroom',methods=['POST'])
def lendClassroom():
    info = dict()
    errors = []
    connection = pymysql.connect(host=cfg['db']['host'],user=cfg['db']['user'],password=cfg['db']['password'],db=cfg['db']['database'])
    cursor=connection.cursor()
    info['classroomID'] = request.json['classroomID']
    info['courseName'] = request.json['courseName']
    schoolname = session.get('schoolName')
    cursor.execute("SELECT userName,phoneNumber from Users WHERE schoolname=%(schoolname)s ", {'schoolname':schoolname})
    rows = cursor.fetchall()
    connection.commit()
    info['userName'] = rows[0][0]
    info['phoneNumber'] = rows[0][1]
    info['lendTime'] = request.json['lendTime']
    info['returnTime'] = request.json['returnTime']
    info['weekDay'] = request.json['weekDay']
    info['reason'] = request.json['reason']
    try:
        print(info['classroomID'])
        cursor.execute("SELECT * from Classrooms WHERE classroomID=%(classroomID)s ", {'classroomID':info['classroomID']})
        rows = cursor.fetchall()
        connection.commit()
        if len(rows) == 0:
            errors.append("No classroom exist!")
            info['errors']=errors
        else:
            insertString = 'INSERT INTO ApplicationForms(classroomID,courseName,userName,schoolName,phoneNumber,lendTime,returnTime,weekDay,reason)values(%(classroomID)s,%(courseName)s,%(userName)s,%(schoolName)s,%(phoneNumber)s,%(lendTime)s,%(returnTime)s,%(weekDay)s,%(reason)s);'
            cursor.execute(insertString,{'classroomID':info['classroomID'],'courseName':info['courseName'],'userName':info['userName'],'schoolName':session.get('schoolName'),'phoneNumber':info['phoneNumber'],'lendTime':info['lendTime'],'returnTime':info['returnTime'],'weekDay':info['weekDay'],'reason':info['reason']})
            connection.commit()
    except Exception: #get exception if there's still occured something wrong
            traceback.print_exc()
            connection.rollback()
            info['errors'] = 'checkLendClassroom fail'
    return jsonify(info)

@ApplicationForms.route('/selectApplicationForms',methods=['POST'])
def selectApplicationForms():
    info = dict()
    errors = []
    connection = pymysql.connect(host=cfg['db']['host'],user=cfg['db']['user'],password=cfg['db']['password'],db=cfg['db']['database'])
    cursor=connection.cursor()
    info['classroomID'] = request.json['classroomID']
    try:
        info['lendTime']=[]
        info['returnTime']=[]
        info['weekDay']=[]
        cursor.execute("SELECT lendTime,returnTime,weekDay from ApplicationForms WHERE classroomID=%(classroomID)s ", {'classroomID':info['classroomID']})
        rows = cursor.fetchall()
        connection.commit()
        for row in rows:
            info['lendTime'].append(row[0])
            info['returnTime'].append(row[1])
            info['weekDay'].append(row[2])
    except Exception: #get exception if there's still occured something wrong
            traceback.print_exc()
            connection.rollback()
            info['errors'] = 'selectApplicationForms fail'
    return jsonify(info)