
from flask import Blueprint
from flask import request,jsonify,json,abort

from app.libs.helper import ops_render
import subprocess
import os
import time

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
