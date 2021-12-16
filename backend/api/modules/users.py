from flask import Blueprint,request,jsonify
import pymysql
import yaml
import re
import traceback
import hashlib
import random
import string
import datetime

#for user register

with open('config.yml', 'r') as f:
    cfg = yaml.safe_load(f)

class CheckForm():

    def __init__(self):
        self.__Errors=[]
    # a letterNumber composed with only letter or number 
    def letterNumberOnly(self,str):
        if re.match("^[A-Za-z0-9]*$", str):
            return True
        return False 
    
    def NumberOnly(self,str):
        if re.match("^[0-9]*$", str):
            return True
        return False 
    #user name shouldn't be empty
    def userName(self,str):
        if len(str)>15 or len(str)<1:
            self.__Errors.append('userName length error')
    #student's ID
    def schoolName(self,str):
        if not self.letterNumberOnly(str):
            self.__Errors.append('schoolName has illegal characters')
        if len(str)>10 or len(str)<5:
            self.__Errors.append('schoolName length error')
    
    def phoneNumber(self,str):
        if not self.NumberOnly(str):
            self.__Errors.append('phoneNumber has illegal characters')
        if len(str)>10 or len(str)<7:
            self.__Errors.append('phoneNumber length error')
    
    def password(self,str):
        if not self.letterNumberOnly(str):
            self.__Errors.append('passwd has illegal characters')
        if len(str)>20 or len(str)<5:
            self.__Errors.append('password length error')
    # password confirm (input password again)
    def passwdConfirm(self,ori,cof):
        if not self.letterNumberOnly(cof):
            self.__Errors.append('passwdConfirm has illegal characters')
        if ori!=cof:
            self.__Errors.append('password diffrent from passwordConfirm')
    # Email = (letter or number) + "@email.ntou.edu.tw"
    # ex. sun1223god@email.ntou.edu.tw
    def Email(self,str):
        if not re.search(r"^[A-Za-z0-9]+@email.ntou.edu.tw$",str):
            self.__Errors.append('Email format error')
    # return the errors after checked all
    def getErrors(self):
        return self.__Errors

class CheckRepeat():
    
    def __init__(self):
        self.__Errors=[]
        self.__cursor = None
    #student's ID shouldn't appear twice
    def schoolName(self,str):
        connection = pymysql.connect(host=cfg['db']['host'],user=cfg['db']['user'],password=cfg['db']['password'],db=cfg['db']['database'])
        self.__cursor = connection.cursor()
        self.__cursor.execute("SELECT * from Users WHERE schoolName = %(schoolName)s",{'schoolName':str})
        rows = self.__cursor.fetchall() #fetch all data from cursor
        if len(rows):
            self.__Errors.append('schoolName has been registered')
    #Email shouldn't appear twice
    def Email(self,str):
        connection = pymysql.connect(host=cfg['db']['host'],user=cfg['db']['user'],password=cfg['db']['password'],db=cfg['db']['database'])
        self.__cursor = connection.cursor()
        self.__cursor.execute("SELECT * from Users WHERE Email = %(Email)s",{'Email':str})
        rows = self.__cursor.fetchall()
        if len(rows):
            self.__Errors.append('Email has been registered')
    #phoneNumber shouldn't appear twice
    def phoneNumber(self,str):
        connection = pymysql.connect(host=cfg['db']['host'],user=cfg['db']['user'],password=cfg['db']['password'],db=cfg['db']['database'])
        self.__cursor = connection.cursor()
        self.__cursor.execute("SELECT * from Users WHERE phoneNumber = %(phoneNumber)s",{'phoneNumber':str})
        rows = self.__cursor.fetchall()
        if len(rows):
            self.__Errors.append('phoneNumber has been registered')
    def getErrors(self):
        return self.__Errors

def checkRegisterRequest(data):
    #init checkForm
    checkForm = CheckForm()
    checkForm.userName(data['userName'])
    checkForm.schoolName(data['schoolName'])
    checkForm.password(data['password'])
    checkForm.phoneNumber(data['phoneNumber'])
    checkForm.passwdConfirm(data['password'],data['passwdConfirm'])
    checkForm.Email(data['Email'])
    #get Errors after checked form
    Errors = checkForm.getErrors()
    #check again (init)
    checkRepeat = CheckRepeat()
    #if Email is legal -> check Email again
    if 'Email has illegal characters' not in Errors and 'Email format error' not in Errors:
        checkRepeat.Email(data['Email'])
    #if schoolName is legal -> check schoolName again
    if 'schoolName has illegal characters' not in Errors and 'schoolName length error' not in Errors:
        checkRepeat.schoolName(data['schoolName'])
    #if phoneNumber is legal -> check phoneNumber again
    if 'phoneNumber has illegal characters' not in Errors and 'phoneNumber length error' not in Errors:
        checkRepeat.phoneNumber(data['phoneNumber'])
    #get the error in checkRepeat
    for error in checkRepeat.getErrors():
        Errors.append(error)

    return Errors

users=Blueprint("users",__name__) 
#for cut path
@users.route('/')
def index():
    return "Users route"

@users.route('/register',methods=['POST'])
def register():
    #get data in form by name from HTML
    connection = pymysql.connect(host=cfg['db']['host'],user=cfg['db']['user'],password=cfg['db']['password'],db=cfg['db']['database'])
    #build dictionary
    info = dict()
    cursor = connection.cursor()
    info['userName'] = request.values.get('userName')
    info['schoolName'] = request.values.get('schoolName')
    info['phoneNumber'] = request.values.get('phoneNumber')
    info['password'] = request.values.get('password')
    info['passwdConfirm'] = request.values.get('passwdConfirm')
    info['Email'] = request.values.get('Email')
    #check info's correctness
    errors = checkRegisterRequest(info)
    #record errors in dictionary
    info['errors'] = errors
    #if there's no error occured in info -> insert the new data to database
    if len(info['errors'])==0:
        try:
            insertString = 'INSERT INTO Users(userName,schoolName,password,phoneNumber,Email,isAdmin,status)values(%(userName)s,%(schoolName)s,%(password)s,%(phoneNumber)s,%(Email)s,%(isAdmin)s,%(status)s)'
            md5 = hashlib.md5() #hash the password for security
            md5.update((request.values.get('password')).encode("utf8")) # for BIG5 and utf8 problem
            cursor.execute(insertString, {'userName':info['userName'], 'schoolName':info['schoolName'],'password': md5.hexdigest(),'phoneNumber':info['phoneNumber'],'Email':info['Email'],'isAdmin':False,'status':0})
            connection.commit() #submit the data to database 
        except Exception: #get exception if there's still occured something wrong
            traceback.print_exc()
            connection.rollback()
            info['errors'] = 'register fail'
    #delete password and password Confirm for security
    del info['password']
    del info['passwdConfirm']

    return jsonify(info)
#@app.before_request
#def make_session_permanent():
#   session.permanent = True
#   app.permanent_session_lifetime = timedelta(minutes=5)

#   email confirm undo
#   if a user input an error email (but legal), his student's ID fucked up. 