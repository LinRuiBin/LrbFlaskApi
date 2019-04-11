
from flask import Blueprint
from flask import request,jsonify,json

from app.libs.helper import ops_render


web_route = Blueprint('web', __name__)

@web_route.route("/",methods = [ "GET","POST" ])
def index():
    return ops_render("common/base.html")
