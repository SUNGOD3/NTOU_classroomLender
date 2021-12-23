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
    info['classroomID'] = request.values.get('classroomID')
    info['equipment1'] = request.values.get('equipment1')
    info['equipment2'] = request.values.get('equipment2')
    info['equipment3'] = request.values.get('equipment3')
    info['equipment4'] = request.values.get('equipment4')
    info['equipment5'] = request.values.get('equipment5')
    try:
        insertString = 'INSERT INTO Classrooms(classroomID,status,equipment1,equipment2,equipment3,equipment4,equipment5)values(%(classroomID)s,%(status)s,%(equipment1)s,%(equipment2)s,%(equipment3)s,%(equipment4)s,%(equipment5)s)'
        cursor.execute(insertString, {'classroomID':info['classroomID'], 'status':0,'equipment1': info['equipment1'],'equipment2':info['equipment2'],'equipment3':info['equipment3'],'equipment4':info['equipment4'],'equipment5':info['equipment5']})
        connection.commit() #submit the data to database 
    except Exception: #get exception if there's still occured something wrong
        traceback.print_exc()
        connection.rollback()
        info['errors'] = 'addClassroom fail'
    return jsonify(info)

@Classrooms.route('/deleteClassroom',methods=['POST'])
def deleteClassroom():
    #get data in form by name from HTML
    connection = pymysql.connect(host=cfg['db']['host'],user=cfg['db']['user'],password=cfg['db']['password'],db=cfg['db']['database'])
    #build dictionary
    info = dict()
    cursor = connection.cursor()
    info['classroomID'] = request.values.get('classroomID')
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
    #get data in form by name from HTML
    connection = pymysql.connect(host=cfg['db']['host'],user=cfg['db']['user'],password=cfg['db']['password'],db=cfg['db']['database'])
    #build dictionary
    info = dict()
    cursor = connection.cursor()
    info['classroomID'] = request.values.get('classroomID')
    info['equipment1'] = request.values.get('equipment1')
    info['equipment2'] = request.values.get('equipment2')
    info['equipment3'] = request.values.get('equipment3')
    info['equipment4'] = request.values.get('equipment4')
    info['equipment5'] = request.values.get('equipment5')
    try:
        cursor.execute('UPDATE Classrooms SET equipment1 = %(equipment1)s, equipment2 = %(equipment2)s, equipment3 = %(equipment3)s, equipment4 = %(equipment4)s, equipment5 = %(equipment5)s WHERE classroomID = %(classroomID)s' ,
                       {'equipment1':info['equipment1'],'equipment2':info['equipment2'],'equipment3':info['equipment3'],'equipment4':info['equipment4'],'equipment5':info['equipment5'],'classroomID':info['classroomID']})
        connection.commit() #submit the data to database
    except Exception: #get exception if there's still occured something wrong
        traceback.print_exc()
        connection.rollback()
        info['errors'] = 'changeClassroom fail'
    return jsonify(info)