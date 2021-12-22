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
    
Scheduler=Blueprint("Scheduler",__name__) 
#for cut path
@Scheduler.route('/')
def index():
    return "Scheduler route"