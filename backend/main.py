
from flask import Flask
from flask import request

import os
from backend.models.tables import  DBSession,Task, Category, Video, session

basedir = os.path.abspath(os.path.dirname(__name__))

app = Flask(__name__)

PAGESIZE = 20

@app.route('/video', methods=['GET'])
def video():
    # fecth the video data from sqlite using sqlachmy orm
    if request.args.get("page"):
        page = int(request.args.get("page"))
    else:
        page = 1
    if request.args.get("pagesize"):
        pagesize = int(request.args.get("pagesize"))
    else:
        pagesize = PAGESIZE

    video_list = session.query(Video).order_by(Video.id.desc())[pagesize*(page-1):pagesize*page]
    videos = [video.serialize() for video in video_list] 

    return {
        "status": "ok",
        "total": 10,
        "msg": "触发成功！",
        "data": videos
    }

@app.route('/category', methods=['GET'])
def category():
    if request.args.get("page"):
        page = int(request.args.get("page"))
    else:
        page = 1
    if request.args.get("pagesize"):
        pagesize = int(request.args.get("pagesize"))
    else:
        pagesize = PAGESIZE

    category_list = session.query(Category).order_by(Category.id.desc())[pagesize*(page-1):pagesize*page]
    categories = [category.serialize() for category in category_list] 
    # the code below is executed if the request method
    # was GET or the credentials were invalid
    return {
        "success": True,
        "msg": "触发成功！",
        "total": 20,
        "data": categories
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
            "file_size": 100,
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
