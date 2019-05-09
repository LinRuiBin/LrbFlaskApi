"""
 Created by LRB on 2018/5/7.
"""
import os
from werkzeug.exceptions import HTTPException

from flask_script import Server
from app import app,manager  #创建app
import common_init
from app.libs.error import APIException,APIResponse
from app.libs.error_code import ServerError
# from app.jobs.tasks.pay import index
# from app.jobs.launcher import runJob

__author__ = 'LRB'

# manager.add_command("runserver", Server( host='0.0.0.0',port=5001,use_debugger = True ,use_reloader = True) )
# manager.add_command('runjob', runJob())

@app.errorhandler(Exception)
def framework_error(e):
    if isinstance(e, APIException):
        return e
    if isinstance(e,APIResponse):
        return e
    if isinstance(e, HTTPException):
        code = e.code
        msg = e.description
        status = 1007
        return APIException(msg, code, status)
    else:
        # 调试模式
        # log
        if not app.config['DEBUG']:
            return ServerError()
        else:
            raise e


if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000)
