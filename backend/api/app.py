# app.py
from flask import Flask ,session,app,request,jsonify
from modules.users import users
import os
from modules.Classrooms import Classrooms
from modules.Email import Email
from modules.Scheduler import Scheduler
from modules.ApplicationForms import ApplicationForms
from modules.history import history
import datetime

app=Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)
app.config['PERMANENT_SESSION_LIFETIME'] =datetime.timedelta(minutes=10)
# 5mins is too short !

@app.route('/')
def index():
    return "Hello Flask"


app.register_blueprint(users,url_prefix='/users')
app.register_blueprint(Classrooms,url_prefix='/Classrooms')
app.register_blueprint(Email,url_prefix='/Email')
app.register_blueprint(Scheduler,url_prefix='/Scheduler')
app.register_blueprint(ApplicationForms,url_prefix='/ApplicationForms')
app.register_blueprint(history,url_prefix='/history')

@app.before_request 
def timeout():
    info = dict()
    if request.path =="/users/login" or request.path =="/users/register"or request.path =="/users/setIdentityCode" or request.path=="/users/checkIdentityCode" or request.path=="/Email/sendEmail":
        return None
    else:
        if not session.get("schoolName"):
            info['errors'] = 'timeout!'
            return jsonify(info)
            

if __name__=='__main__':
    app.run(port='13588')