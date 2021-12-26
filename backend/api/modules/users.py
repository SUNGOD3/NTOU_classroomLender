from ctypes import sizeof
from flask import Blueprint,request,jsonify,url_for,redirect,render_template,session
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
            self.__Errors.append('password has illegal characters')
        if len(str)>20 or len(str)<5:
            self.__Errors.append('password length error')
    # password confirm (input password again)
    def passwdConfirm(self,ori,cof):
        if not self.letterNumberOnly(cof):
            self.__Errors.append('passwdConfirm has illegal characters')
        if ori!=cof:
            self.__Errors.append('password diffrent from passwordConfirm')
    # Email = (letter or number) + "@mail.ntou.edu.tw"
    # ex. sun1223god@mail.ntou.edu.tw
    def Email(self,str):
        if not re.search(r"^[A-Za-z0-9]+@mail.ntou.edu.tw$",str):
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

class CheckEmail():
    def __init__(self):
        self.__Errors=[]

    def schoolName(self,str):
        connection = pymysql.connect(host=cfg['db']['host'],user=cfg['db']['user'],password=cfg['db']['password'],db=cfg['db']['database'])
        cursor = connection.cursor()
        cursor.execute("SELECT * from Users WHERE schoolName = %(schoolName)s",{'schoolName':str})
        rows = cursor.fetchall()
        if not len(rows):
            self.__Errors.append('schoolName has not found')

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
CORS(users)
#for cut path
@users.route('/')
def index():
    return "Users route"

@users.route('/register',methods=['POST'])
def register():
    #connect to mysql
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
            insertString = 'INSERT INTO Users(userName,schoolName,password,phoneNumber,Email,isAdmin,status,apply)values(%(userName)s,%(schoolName)s,%(password)s,%(phoneNumber)s,%(Email)s,%(isAdmin)s,%(status)s,%(apply)s)'
            md5 = hashlib.md5() #hash the password for security
            md5.update((request.values.get('password')).encode("utf8")) # for BIG5 and utf8 problem
            cursor.execute(insertString, {'userName':info['userName'], 'schoolName':info['schoolName'],'password': md5.hexdigest(),'phoneNumber':info['phoneNumber'],'Email':info['Email'],'isAdmin':False,'status':0,'apply':0})
            connection.commit() #submit the data to database 
        except Exception: #get exception if there's still occured something wrong
            traceback.print_exc()
            connection.rollback()
            info['errors'] = 'register fail'
    #delete password and password Confirm for security
    del info['password']
    del info['passwdConfirm']
    #return render_template('register.html')
    return jsonify(info)

@users.route('/login',methods=['POST'])
def login():
    connection = pymysql.connect(host=cfg['db']['host'],user=cfg['db']['user'],password=cfg['db']['password'],db=cfg['db']['database'])
    info = dict()
    schoolName = request.values.get('schoolName')
    password = request.values.get('password')
    cursor = connection.cursor()
    cursor.execute("SELECT * from Users WHERE schoolName = %(schoolName)s",{'schoolName':schoolName})
    rows = cursor.fetchall()
    connection.commit()
    Errors = []
    if not len(rows):
        Errors.append('schoolName doesn\'t exist')
    else:
        cursor.execute("SELECT * from Users WHERE schoolName = %(schoolName)s",{'schoolName':schoolName})
        rows = cursor.fetchall()
        connection.commit()
        row = rows[0]
        md5 = hashlib.md5()
        md5.update(password.encode("utf8"))
        # ! password current index is 2
        if md5.hexdigest() == row[2]:
            session.permanent = True
            #add a schoolName into session use session to timeout
            session['schoolName']=row[1]
        else:
            Errors.append('password error')
        info['isAdmin'] = row[5]

    info['errors'] = Errors
    return jsonify(info)

@users.route('/setIdentityCode',methods=['POST'])
def setIdentityCode():
    connection = pymysql.connect(host=cfg['db']['host'],user=cfg['db']['user'],password=cfg['db']['password'],db=cfg['db']['database'])
    info = dict()
    cursor = connection.cursor()
    schoolName = request.values.get('schoolName')
    cursor.execute("SELECT * from Users WHERE schoolName = %(schoolName)s",{'schoolName':schoolName})
    checkEmail=CheckEmail()
    checkEmail.schoolName(schoolName)
    info['errors'] = checkEmail.getErrors()
    connection.commit()
    if len(info['errors'])==0:
        info['schoolName'] = schoolName
        try:
            identityCode = ""
            for i in range(6):
                tmp=random.randint(0,2)
                if tmp==0:
                    tmp=random.randint(0,9)
                    identityCode += str(tmp)
                elif tmp==1:
                    tmp=random.randint(65,90)
                    identityCode += chr(tmp)
                else :
                    tmp=random.randint(97,122)
                    identityCode += chr(tmp)
            cursor.execute("UPDATE Users SET identityCode = %(identityCode)s WHERE schoolName = %(schoolName)s",{'identityCode':identityCode,'schoolName':schoolName})
            connection.commit()
        except Exception:
            traceback.print_exc()
            connection.rollback()
            info['errors'] = 'setIdentityCode fail'
    return jsonify(info)

@users.route('/checkIdentityCode',methods=['POST'])
def checkIdentityCode():
    connection = pymysql.connect(host=cfg['db']['host'],user=cfg['db']['user'],password=cfg['db']['password'],db=cfg['db']['database'])
    info = dict()
    errors=[]
    cursor = connection.cursor()
    schoolName = request.values.get('schoolName')
    identityCode=request.values.get('identityCode')
    cursor.execute("SELECT identityCode from Users WHERE schoolName = %(schoolName)s",{'schoolName':schoolName})
    rows = cursor.fetchall()
    connection.commit()
    if rows[0][0]!=identityCode:
        errors.append('identityCode error')
    else:
        session.permanent = True
        #add a schoolName into session use session to timeout
        session['schoolName']=request.values.get('schoolName')
    info['errors']=errors
    return jsonify(info)

def checkPassWord(data):
    checkForm = CheckForm()
    checkForm.password(data['password'])
    checkForm.passwdConfirm(data['password'],data['passwdConfirm'])
    Errors = checkForm.getErrors()
    return Errors

@users.route('/resetPassword',methods=['POST'])
def resetPassword():
    connection = pymysql.connect(host=cfg['db']['host'],user=cfg['db']['user'],password=cfg['db']['password'],db=cfg['db']['database'])
    info = dict()
    errors=[]
    cursor=connection.cursor()
    info['password'] = request.values.get('password')
    info['passwdConfirm'] = request.values.get('passwdConfirm')
    errors = checkPassWord(info)
    if session.get('schoolName')==None:
        errors.append('not pass identityCode yet!')
    info['errors'] = errors
    if len(info['errors'])==0:
        try:
            md5 = hashlib.md5()
            md5.update((request.values.get('password')).encode("utf8"))
            cursor.execute("UPDATE Users SET password = %(password)s WHERE schoolName = %(schoolName)s", {'password':md5.hexdigest(),'schoolName':session.get('schoolName')})
            connection.commit()
        except Exception:
            traceback.print_exc()
            connection.rollback()
            info['errors'] = 'reset fail'
    del info['password']
    del info['passwdConfirm']
    return jsonify(info)

@users.route('/applyForManager',methods=['POST'])
def applyForManager():
    connection = pymysql.connect(host=cfg['db']['host'],user=cfg['db']['user'],password=cfg['db']['password'],db=cfg['db']['database'])
    info = dict()
    errors=[]
    cursor=connection.cursor()
    if session.get('schoolName')==None:
        info['errors'] = 'timeout!'
    else:
        try:
            cursor.execute("UPDATE Users SET apply = %(apply)s WHERE schoolName = %(schoolName)s", {'apply':1,'schoolName':session.get('schoolName')})
            connection.commit()
        except Exception:
            traceback.print_exc()
            connection.rollback()
            info['errors'] = 'apply fail'
    return jsonify(info)

@users.route('/checkAllUser',methods=['GET'])
def checkAllUser():
    info = dict()
    errors = []
    connection = pymysql.connect(host=cfg['db']['host'],user=cfg['db']['user'],password=cfg['db']['password'],db=cfg['db']['database'])
    cursor=connection.cursor()
    cursor.execute("SELECT schoolName,userName,status,Email from Users ")
    rows = cursor.fetchall()
    connection.commit()
    if len(rows) == 0:
        errors.append("No user exist!")
    else:
        info['users'] = []
        for row in rows:
            info['users'].append(""+row[0]+","+row[1]+","+str(row[2])+","+row[3])
    info['errors'] = errors
    return jsonify(info)

@users.route('/confirmApply',methods=['GET'])
def confirmApply():
    info = dict()
    errors = []
    connection = pymysql.connect(host=cfg['db']['host'],user=cfg['db']['user'],password=cfg['db']['password'],db=cfg['db']['database'])
    cursor=connection.cursor()
    cursor.execute("SELECT schoolName,userName from Users WHERE apply=1")
    rows = cursor.fetchall()
    connection.commit()
    if len(rows) == 0:
        errors.append("No one apply!")
    else:
        info['users'] = []
        for row in rows:
            info['users'].append(""+row[0]+","+row[1])
    info['errors'] = errors
    return jsonify(info)

@users.route('/postConfirm',methods=['POST'])
def postConfirm():
    info = dict()
    info['schoolName'] = request.values.get('schoolName')
    connection = pymysql.connect(host=cfg['db']['host'],user=cfg['db']['user'],password=cfg['db']['password'],db=cfg['db']['database'])
    cursor=connection.cursor()
    cursor.execute("UPDATE Users SET isAdmin =%(isAdmin)s , apply =%(apply)s WHERE schoolName=%(schoolName)s",{'isAdmin': 1,'apply': 0,'schoolName':info['schoolName']})
    connection.commit()
    return jsonify(info)

@users.route('/postReject',methods=['POST'])
def postReject():
    info = dict()
    info['schoolName'] = request.values.get('schoolName')
    connection = pymysql.connect(host=cfg['db']['host'],user=cfg['db']['user'],password=cfg['db']['password'],db=cfg['db']['database'])
    cursor=connection.cursor()
    cursor.execute("UPDATE Users SET apply =%(apply)s WHERE schoolName=%(schoolName)s",{'apply': 0,'schoolName':info['schoolName']})
    connection.commit()
    return jsonify(info)


@users.route('/checkLendClassroom',methods=['POST'])
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
        info['lendTime'] = datetime.date.today()
        info['courseName'] = rows[0][0]
        info['userName'] = rows[0][1]
        info['reason'] = rows[0][2]
        #print(rows)
        #insert new data to history
        insertString = 'INSERT INTO History(classroomID,courseName,userName,schoolName,lendTime,returnTime,reason)values(%(classroomID)s,%(courseName)s,%(userName)s,%(schoolName)s,%(lendTime)s,NULL,%(reason)s);'
        cursor.execute(insertString,{'classroomID':info['classroomID'],'courseName':info['courseName'],'userName':info['userName'],'schoolName':info['schoolName'],'lendTime':info['lendTime'],'reason':info['reason']})
        connection.commit()
    except Exception: #get exception if there's still occured something wrong
            traceback.print_exc()
            connection.rollback()
            info['errors'] = 'checkLendClassroom fail'
    return jsonify(info)

@users.route('/info',methods=['POST'])
def info():
    connection = pymysql.connect(host=cfg['db']['host'],user=cfg['db']['user'],password=cfg['db']['password'],db=cfg['db']['database'])
    info = dict()
    errors=[]
    cursor=connection.cursor()
    info['userName'] = request.values.get('userName')
    info['phoneNumber'] = request.values.get('phoneNumber')
    info['password'] = request.values.get('password')
    try:
        if len(info['userName'])>0:
            cursor.execute("UPDATE Users SET userName=%(userName)s  WHERE schoolName = %(schoolName)s",{'userName':info['userName'],'schoolName':session.get('schoolName')})
            connection.commit()
        if len(info['phoneNumber'])>0:
            cursor.execute("UPDATE Users SET phoneNumber=%(phoneNumber)s  WHERE schoolName = %(schoolName)s",{'phoneNumber':info['phoneNumber'],'schoolName':session.get('schoolName')})
            connection.commit()
        if len(info['password'])>0:
            md5 = hashlib.md5()
            md5.update((request.values.get('password')).encode("utf8"))
            checkForm = CheckForm()
            checkForm.password(info['password'])
            errors = checkForm.getErrors()
            info['errors'] = errors
            if len(info['errors'])==0:
                cursor.execute("UPDATE Users SET password=%(password)s  WHERE schoolName = %(schoolName)s",{'password':md5.hexdigest(),'schoolName':session.get('schoolName')})
                connection.commit()
    except Exception:
            traceback.print_exc()
            connection.rollback()
            info['errors'] = 'modify fail'
    del info['password']
    return jsonify(info)
    
@users.route('/checkAllManager',methods=['GET'])
def checkAllManager():
    info = dict()
    errors = []
    connection = pymysql.connect(host=cfg['db']['host'],user=cfg['db']['user'],password=cfg['db']['password'],db=cfg['db']['database'])
    cursor=connection.cursor()
    cursor.execute("SELECT schoolName,userName from Users WHERE isAdmin>0")
    rows = cursor.fetchall()
    connection.commit()
    if len(rows) == 0:
        errors.append("No manager!")
    else:
        info['users'] = []
        for row in rows:
            info['users'].append(""+row[0]+","+row[1])
    info['errors'] = errors
    return jsonify(info)

@users.route('/downGrade',methods=['POST'])
def downGrade():
    info = dict()
    info['schoolName'] = request.values.get('schoolName')
    connection = pymysql.connect(host=cfg['db']['host'],user=cfg['db']['user'],password=cfg['db']['password'],db=cfg['db']['database'])
    cursor=connection.cursor()
    cursor.execute("UPDATE Users SET isAdmin =%(isAdmin)s WHERE schoolName=%(schoolName)s AND isAdmin=1",{'isAdmin': 0,'schoolName':info['schoolName']})
    connection.commit()
    return jsonify(info)

#   email confirm undo
#   if a user input an error email (but legal), his student's ID fucked up. 

#   html should alert if sign up failed when reload