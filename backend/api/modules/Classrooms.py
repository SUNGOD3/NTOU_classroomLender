from os import error
from pymysql.cursors import Cursor
from flask import Blueprint,request,jsonify,session
import pymysql
import yaml
import re
import traceback
import hashlib
import random
import string
import datetime

with open('config.yml', 'r') as f:
    cfg = yaml.safe_load(f)

Classrooms=Blueprint("Classrooms",__name__) 
#for cut path
@Classrooms.route('/')
def index():
    return "Classrooms route"

@Classrooms.route('/addClassroom',methods=['POST'])
def addClassroom():
    #get data in form by name from HTML
    connection = pymysql.connect(host=cfg['db']['host'],user=cfg['db']['user'],password=cfg['db']['password'],db=cfg['db']['database'])
    #build dictionary
    info = dict()
    cursor = connection.cursor()
    info['classroomID'] = request.json['classroomID']
    info['commonEquipment'] = request.json['commonEquipment']
    info['specialEquipment'] = request.json['specialEquipment']
    try:
        insertString = 'INSERT INTO Classrooms(classroomID,status,commonEquipment,specialEquipment)values(%(classroomID)s,%(status)s,%(commonEquipment)s,%(specialEquipment)s)'
        cursor.execute(insertString, {'classroomID':info['classroomID'], 'status':0,'commonEquipment':info['commonEquipment'],'specialEquipment':info['specialEquipment']})
        connection.commit() #submit the data to database 
    except Exception: #get exception if there's still occured something wrong
        traceback.print_exc()
        connection.rollback()
        info['errors'] = 'addClassroom fail'
    return jsonify(info)

@Classrooms.route('/deleteClassroom',methods=['POST'])
def deleteClassroom():
    #get data in form by name from mySQL
    connection = pymysql.connect(host=cfg['db']['host'],user=cfg['db']['user'],password=cfg['db']['password'],db=cfg['db']['database'])
    #build dictionary
    info = dict()
    cursor = connection.cursor()
    info['classroomID'] = request.json['schoolName']
    try:
        cursor.execute("DELETE from Classrooms Where classroomID = %(classroomID)s",{'classroomID':info['classroomID']})
        connection.commit() #submit the data to database 
    except Exception: #get exception if there's still occured something wrong
        traceback.print_exc()
        connection.rollback()
        info['errors'] = 'deleteClassroom fail'
    return jsonify(info)

@Classrooms.route('/changeClassroom',methods=['POST'])
def changeClassroom():
    #get data in form by name from mySQL
    connection = pymysql.connect(host=cfg['db']['host'],user=cfg['db']['user'],password=cfg['db']['password'],db=cfg['db']['database'])
    #build dictionary
    info = dict()
    cursor = connection.cursor()
    info['classroomID'] = request.json['classroomID']
    info['commonEquipment'] = request.json['commonEquipment']
    info['classroomID'] = request.json['classroomID']
    try:
        cursor.execute('UPDATE Classrooms SET  WHERE classroomID = %(classroomID)s' ,
                       {'classroomID':info['classroomID']})
        connection.commit() #submit the data to database
    except Exception: #get exception if there's still occured something wrong
        traceback.print_exc()
        connection.rollback()
        info['errors'] = 'changeClassroom fail'
    return jsonify(info)

@Classrooms.route('/selectClassroom',methods=['POST'])
def selectClassroom():
    #get data in form by name from mySQL
    connection = pymysql.connect(host=cfg['db']['host'],user=cfg['db']['user'],password=cfg['db']['password'],db=cfg['db']['database'])
    #build dictionary
    info = dict()
    errors = []
    cursor = connection.cursor()
    info['classroomID'] = request.json['schoolName']
    try:
        insertString = ('SELECT status from Classrooms where classroomID=%(classroomID)s')
        cursor.execute(insertString,{'classroomID':info['classroomID']})
        rows = cursor.fetchall()
        connection.commit()
        if len(rows) == 0:
            errors.append("No classroom found!")
        elif len(rows) > 1:
            errors.append("Unexpect error:two or more classroom have same ID!")
        else:
            info['status'] = rows[0][0]
            if info['status'] == 1:
                insertString = ('SELECT courseName from History where classroomID=%(classroomID)s and returnTime IS NULL' )
                cursor.execute(insertString,{'classroomID':info['classroomID']})
                rows = cursor.fetchall()
                connection.commit()
                if len(rows) == 0:
                    errors.append("Unexpect error:Classroom has been lent,but history can't find up!")
                info['courseName'] = rows
            else:
                info['courseName'] = "NULL"
    except Exception:
        traceback.print_exc()
        connection.rollback()
        errors.append('Select fail')
    info['errors'] = errors
    return jsonify(info)

@Classrooms.route('/changeClassroomStatus',methods=['POST'])
def changeClassroomStatus():
    #get data in form by name from mySQL
    connection = pymysql.connect(host=cfg['db']['host'],user=cfg['db']['user'],password=cfg['db']['password'],db=cfg['db']['database'])
    #build dictionary
    info = dict()
    cursor = connection.cursor()
    info['classroomID'] = request.json['schoolName']
    info['status'] = request.json['status']
    try:
        cursor.execute('UPDATE Classrooms SET status=%(status)s WHERE classroomID=%(classroomID)s',
                       {'status':info['status'],'classroomID':info['classroomID']})
        connection.commit() #update the data in database
    except Exception: #get exception if there's still occured something wrong
        traceback.print_exc()
        connection.rollback()
        info['errors'] = 'changeClassroomStatus fail'
    return jsonify(info)
    
@Classrooms.route('/searchKeyword',methods=['POST'])
def searchKeyword():
    connection = pymysql.connect(host=cfg['db']['host'],user=cfg['db']['user'],password=cfg['db']['password'],db=cfg['db']['database'])
    #build dictionary
    info = dict()
    cursor = connection.cursor()
    info['searchWord'] = request.json['searchWord']
    try:
        cursor.execute('SELECT specialEquipment,classroomID from Classrooms')
        rows = cursor.fetchall()
        connection.commit() #update the data in database
        info['class'] = []
        for row in rows:
            if info['searchWord'] in row[0] :
                info['class'].append(row[1])
        cursor.execute('SELECT classroomID from Scheduler')
        rows = cursor.fetchall()
        connection.commit() #update the data in database
        for row in rows:
            if info['searchWord'] in row[0] :
                if row[0] not in info['class'] :
                    info['class'].append(row[0])
    except Exception: #get exception if there's still occured something wrong
        traceback.print_exc()
        connection.rollback()
        info['errors'] = 'search fail'
    return jsonify(info)

@Classrooms.route('/equipmentFilter',methods=['POST'])
def equipmentFilter():
    connection = pymysql.connect(host=cfg['db']['host'],user=cfg['db']['user'],password=cfg['db']['password'],db=cfg['db']['database'])
    #build dictionary
    info = dict()
    cursor = connection.cursor()
    info['commonEquipment'] = request.json['commonEquipment']
    try:
        cursor.execute('SELECT commonEquipment,classroomID from Classrooms')
        rows = cursor.fetchall()
        connection.commit()  #update the data in database
        info['class'] = []
        for row in rows: #string
            ac = 1
            for i in range(4):
                if info['commonEquipment'][i] == '1' and row[0][i] == '0':
                    ac = 0
            if ac == 1:
                info['class'].append(row[1])
    except Exception: #get exception if there's still occured something wrong
        traceback.print_exc()
        connection.rollback()
        info['errors'] = 'search fail'
    return jsonify(info)