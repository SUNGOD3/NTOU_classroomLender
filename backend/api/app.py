# app.py
from flask import Flask ,session,app
from modules.users import users
#from modules.Classrooms import Classrooms
#from modules.Email import Email
#from modules.Scheduler import Scheduler
#from modules.ApplicationForms import ApplicationForms
import datetime

app=Flask(__name__)

@app.route('/')
def index():
    return "Hello Flask"


app.register_blueprint(users,url_prefix='/users')
#app.register_blueprint(Classrooms,url_prefix='/Classrooms')
#app.register_blueprint(Email,url_prefix='/Email')
#app.register_blueprint(Scheduler,url_prefix='/Scheduler')
#app.register_blueprint(ApplicationForms,url_prefix='/ApplicationForms')

if __name__=='__main__':
    app.run(port='13588')