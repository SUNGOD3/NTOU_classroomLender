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
    
ApplicationForms=Blueprint("ApplicationForms",__name__) 
#for cut path
@ApplicationForms.route('/')
def index():
    return "ApplicationForms route"