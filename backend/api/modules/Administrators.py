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

Administrators=Blueprint("Administrators",__name__) 
#for cut path
@Administrators.route('/')
def index():
    return "Administrators route"