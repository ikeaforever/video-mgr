
from flask import Flask
from flask import request

import os 
from flask_sqlalchemy import SQLAlchemy
basedir = os.path.abspath(os.path.dirname(__name__))


app = Flask(__name__)

@app.route('/video', methods=['GET'])
def video():
    return {
        "status": "ok",
        "code": 0,
        "msg": "触发成功！",
        "data": [
            {
                "id": 1,
                "name": "视频1",
                "fileszize": 100,
                "transcode_size": 100
            },
            {
                "id": 2,
                "name": "视频2",
                "fileszize": 100,
                "transcode_size": 100
            }
        ]
    }

@app.route('/category', methods=['GET'])
def category():

    # the code below is executed if the request method
    # was GET or the credentials were invalid
    return {
        "status": "ok",
        "code": 0,
        "msg": "触发成功！",
        "data": [
            {
                "id": 1,
                "name": "分类1"
            },
            {
                "id": 2,
                "name": "分类2"
            },
            {
                "id": 3,
                "name": "分类"
            }
        ]
    }

@app.route('/total', methods=['GET'])
def total():

    # the code below is executed if the request method
    # was GET or the credentials were invalid
    return {
        "status": "ok",
        "code": 0,
        "msg": "触发成功！",
        "data": {
            "total": 100,
            "transcode_size": 100
        }
    }

@app.route("/task", methods=[ 'POST'])
def task():
    return {
        "status": "ok",
        "code": 0,
        "msg": u"触发成功！"
    }

@app.route("/")
def index():
    return "Hello World!"