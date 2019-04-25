
from flask import Blueprint
from flask import request,jsonify,json,abort

from app.libs.helper import ops_render
import subprocess
import os

web_route = Blueprint('web', __name__)

@web_route.route("/",methods = [ "GET","POST" ])
def index():
    return ops_render("common/base.html")


#版本更新
@web_route.route("/githook",methods = [ "GET","POST" ])
def githook():
    if request.method == "POST":
        # retcode = subprocess.call("cd /home/FlaskProject/LrbFlaskApi && git checkout . && git pull")
        retcode = os.system("cd /home/FlaskProject/LrbFlaskApi && git checkout . && git pull")
        if retcode == 0:
            return jsonify({"status":"success"},200)
        else:
            return jsonify({"status": "error"}, 503)

    else:
        abort(400)