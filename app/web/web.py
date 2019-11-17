
from flask import Blueprint
from flask import request,jsonify,json,abort

from app.libs.helper import ops_render
import subprocess
import os
import time

from  app.models.userOrder import *

web_route = Blueprint('web', __name__)

@web_route.route("/",methods = [ "GET","POST" ])
def index():
    return ops_render("common/base.html")


#版本更新
@web_route.route("/githook",methods = [ "GET","POST" ])
def githook():
    if request.method == "POST":
        # retcode = subprocess.call("cd /home/FlaskProject/LrbFlaskApi && git checkout . && git pull")
        os.system("cd /home/FlaskProject/LrbFlaskApi && git checkout . && git pull")
        # arg = ' restart'
        # time.sleep(5)
        # os.system('./uwsgiServer.sh restart')
        return jsonify({"status":"success"},200)

@web_route.route("/search/",methods = [ "GET","POST" ])
def search():
    if request.method == 'GET':
        return ops_render("web/searchInfo.html")

    if request.method == 'POST':
        re = request
        form =request.form
        name = form['name']
        studynum = form['study_num']
        allmodel = User_Order_Info.query.all()
        info_model = User_Order_Info.query.filter(User_Order_Info.study_Id==studynum,User_Order_Info.name==name).first()
        result_dict = {}
        if info_model:
            result_dict['name'] = info_model.name
            result_dict['study_num'] = info_model.study_Id
            result_dict['money'] = info_model.money
            result_dict['order_num'] = info_model.order_num

        return ops_render("web/searchResult.html",context={'info':result_dict})