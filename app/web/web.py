
from flask import Blueprint
from flask import request,jsonify,json,abort

from app.libs.helper import ops_render
import subprocess

web_route = Blueprint('web', __name__)

@web_route.route("/",methods = [ "GET","POST" ])
def index():
    return ops_render("common/base.html")


#版本更新
@web_route.route("/githook",methods = [ "GET","POST" ])
def githook():
    if request.method == "POST":
        return jsonify({"status": "success"}, 200)
        # retcode = subprocess.call("cd /home/FlaskProject/LrbFlaskApi && git checkout . && git pull && /bin/bash uwsgiServer.sh restart")
        # if retcode == 0:
        #     return jsonify({"status":"success"},200)
        # else:
        #     return jsonify({"status": "error"}, 503)

    else:
        abort(400)