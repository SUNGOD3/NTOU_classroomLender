from flask import Blueprint,request,jsonify,session
import pymysql
import yaml
import re
import traceback
import hashlib
import random
import string
import datetime
from flask_cors import CORS

with open('config.yml', 'r') as f:
    cfg = yaml.safe_load(f)
    
ApplicationForms=Blueprint("ApplicationForms",__name__) 
CORS(ApplicationForms)

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
    cursor.execute("SELECT schoolName,userName,classroomID,lendTime,returnTime,weekDay from ApplicationForms")
    rows = cursor.fetchall()
    connection.commit()
    if len(rows) == 0:
        errors.append("No ApplicationForms exist!")
    else:
        info['data'] = []
        for row in rows:
            info['data'].append(""+row[0]+","+row[1]+","+row[2]+","+str(row[3])+","+str(row[4])+','+str(row[5]))
    info['errors'] = errors
    return jsonify(info)