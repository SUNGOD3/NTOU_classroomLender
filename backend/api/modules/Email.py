from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from flask import Blueprint,request,jsonify,session
import pymysql
import yaml
import traceback
import string
import smtplib
from flask_cors import CORS

with open('config.yml', 'r') as f:
    cfg = yaml.safe_load(f)

with open('GmailConfig.yml','r') as a:
    mailUserData=yaml.safe_load(a)

GmailAccount=mailUserData['GmailAccount']['Account']
Gmailpasswd=mailUserData['GmailAccount']['password']

Email=Blueprint("Email",__name__)
CORS(Email,resources={r"/*": {"origins": "*"}},supports_credentials=True)

@Email.route('/')
def index():
    return "Email route"

@Email.route('/sendEmail',methods=['POST'])    
def sendEmail():
    connection = pymysql.connect(host=cfg['db']['host'],user=cfg['db']['user'],password=cfg['db']['password'],db=cfg['db']['database'])
    info = dict()
    cursor = connection.cursor()
    Email = request.json['Email']
    cursor.execute("SELECT identityCode from Users WHERE Email = %(Email)s",{'Email':Email})
    rows = cursor.fetchall()
    connection.commit()
    if not len(rows):
           info['errors']='Email doesn\'t exist'
    else:
        content = MIMEMultipart()  #建立MIMEMultipart物件
        content["subject"] = "NTOU_classroomLender"  #郵件標題
        content["from"] = mailUserData['GmailAccount']['Account']  #寄件者
        content["to"] = Email#收件者
        message='your identityCode is '+rows[0][0]
        content.attach(MIMEText(message))  #郵件內容
        with smtplib.SMTP(host="smtp.gmail.com", port="587") as smtp:  # 設定SMTP伺服器
            try:
                smtp.ehlo()  # 驗證SMTP伺服器
                smtp.starttls()  # 建立加密傳輸
                smtp.login(GmailAccount, Gmailpasswd)  # 登入寄件者gmail
                smtp.send_message(content)  # 寄送郵件
                print('Sent message successfully....')
                info['errors']=''
            except Exception as e:
                info['errors']='Sent message failed'
                e.traceback()
        info['email']=Email
        return jsonify(info)
