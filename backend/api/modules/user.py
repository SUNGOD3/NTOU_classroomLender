from flask import Blueprint,request,jsonify
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

class CheckForm():
    global connection

    def __init__(self):
        self.__Errors=[]

    def letterNumberOnly(self,str):
        if re.match("^[A-Za-z0-9]*$", str):
            return True
        return False 

    def schoolName(self,str):
        if not self.letterNumberOnly(str):
            self.__Errors.append('schoolName has illegal characters')
        if len(str)>10 or len(str)<5:
            self.__Errors.append('schoolName length error')
        
    def phonenumber(self,str):
        if not re.match("^[0-9]", str):
            self.__Errors.append('phonenumber has illegal characters')
        if len(str)>10 or len(str)<7:
            self.__Errors.append('phonenumber length error')
    
    def password(self,str):
        if not self.letterNumberOnly(str):
            self.__Errors.append('passwd has illegal characters')
        if len(str)>20 or len(str)<5:
            self.__Errors.append('password length error')

    def passwdConfirm(self,ori,cof):
        if not self.letterNumberOnly(cof):
            self.__Errors.append('passwdConfirm has illegal characters')
        if ori!=cof:
            self.__Errors.append('password diffrent from passwordConfirm')

    def Email(self,str):
        if not re.search(r"^[A-Za-z0-9]+@ntou.edu.tw$",str):
            self.__Errors.append('Email format error')

    def getErrors(self):
        return self.__Errors

class CheckRepeat():
    
    def __init__(self):
        self.__Errors=[]
        self.__cursor = None
    def schoolName(self,str):
        connection = pymysql.connect(host=cfg['db']['host'],user=cfg['db']['user'],password=cfg['db']['password'],db=cfg['db']['database'])
        self.__cursor = connection.cursor()
        self.__cursor.execute("SELECT * from Users WHERE schoolName = %(schoolName)s",{'schoolName':str})
        rows = self.__cursor.fetchall()
        if len(rows):
            self.__Errors.append('schoolName has been registered')

    def Email(self,str):

        connection = pymysql.connect(host=cfg['db']['host'],user=cfg['db']['user'],password=cfg['db']['password'],db=cfg['db']['database'])
        self.__cursor = connection.cursor()
        self.__cursor.execute("SELECT * from Users WHERE Email = %(Email)s",{'Email':str})
        rows = self.__cursor.fetchall()
        if len(rows):
            self.__Errors.append('Email has been registered')
    
    def phonenumber(self,str):
    
        connection = pymysql.connect(host=cfg['db']['host'],user=cfg['db']['user'],password=cfg['db']['password'],db=cfg['db']['database'])
        self.__cursor = connection.cursor()
        self.__cursor.execute("SELECT * from Users WHERE phonenumber = %(phonenumber)s",{'phonenumber':str})
        rows = self.__cursor.fetchall()
        if len(rows):
            self.__Errors.append('phonenumber has been registered')
    def getErrors(self):
        return self.__Errors

def checkRegisterRequest(data):
    checkForm = CheckForm()
    checkForm.schoolName(data['schoolName'])
    checkForm.password(data['passwd'])
    checkForm.phonenumber(data['phonenumber'])
    checkForm.passwdConfirm(data['passwd'],data['passwdConfirm'])
    checkForm.Email(data['Email'])
    Errors = checkForm.getErrors()
    checkRepeat = CheckRepeat()
    if 'Email has illegal characters' not in Errors and 'Email format error' not in Errors:
        checkRepeat.email(data['email'])
    if 'schoolName has illegal characters' not in Errors and 'schoolName length error' not in Errors:
        checkRepeat.schoolName(data['schoolName'])
    if 'phonenumber has illegal characters' not in Errors and 'phonenumber length error' not in Errors:
        checkRepeat.phonenumber(data['phonenumber'])
    for error in checkRepeat.getErrors():
        Errors.append(error)

    return Errors
users=Blueprint("users",__name__)

@user.route('/')
def index():
    return "Users route"

@user.route('/register',methods=['POST'])
def register():
    connection = pymysql.connect(host=cfg['db']['host'],user=cfg['db']['user'],password=cfg['db']['password'],db=cfg['db']['database'])
    info = dict()
    cursor = connection.cursor()
    info['userName'] = request.values.get('userName')
    info['schoolName'] = request.values.get('schoolName')
    info['phoneNumber'] = request.values.get('phoneNumber')
    info['password'] = request.values.get('password')
    info['passwdConfirm'] = request.values.get('passwdConfirm')
    info['email'] = request.values.get('email')
    errors = checkRegisterRequest(info)

    info['errors'] = errors

    if len(info['errors'])==0:
        try:
            insertString = 'INSERT INTO Users(userName,schoolName,password,phoneNumber,Email,isAdmin,status)values(%(userName)s,%(schoolName)s,%(password)s,%(phoneNumber)s,%(Email)s,%(isAdmin)s,%(status)s)'
            md5 = hashlib.md5()
            md5.update((request.values.get('password')).encode("utf8"))
            cursor.execute(insertString, {'userName':info['userName'], 'schoolName':info['schoolName'],'password': md5.hexdigest(),'phoneNumber':info['phoneNumber'],'Email':info['Email'],'isAdmin':False,'status':0})
            connection.commit()
        except Exception:
            traceback.print_exc()
            connection.rollback()
            info['errors'] = 'register fail'

    del info['passwd']
    del info['passwdConfirm']

    return jsonify(info)
@app.before_request
def make_session_permanent():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=5)
