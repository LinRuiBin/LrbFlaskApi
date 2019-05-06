"""
 Created by LRB on 2018/5/7.
"""
from werkzeug.exceptions import HTTPException
from app import create_app  #创建app

from app.libs.error import APIException,APIResponse
from app.libs.error_code import ServerError
from flask_script import Manager

__author__ = 'LRB'
app = create_app()
manager = Manager(app)

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
