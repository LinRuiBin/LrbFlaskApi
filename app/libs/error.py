"""
 Created by LRB on 2018/5/7.

"""
from flask import request, json
from werkzeug.exceptions import HTTPException

__author__ = 'LRB'


class APIException(HTTPException):
    code = 500
    msg = 'sorry, we made a mistake (*￣︶￣)!'
    status = 999
    data = {}
    def __init__(self, msg=None, code=None, status=None,
                 headers=None):
        if code:
            self.code = code
        if status:
            self.status = status
        if msg:
            self.msg = msg
        super(APIException, self).__init__(msg, None)

    def get_body(self, environ=None):
        body = dict(
            msg=self.msg,
            status=self.status,
            request=request.method + ' ' + self.get_url_no_param()
        )
        text = json.dumps(body)
        return text

    def get_headers(self, environ=None):
        """Get a list of headers."""
        return [('Content-Type', 'application/json')]

    @staticmethod
    def get_url_no_param():
        full_path = str(request.full_path)
        main_path = full_path.split('?')
        return main_path[0]


class APIResponse(HTTPException):
    code = 200
    msg = '操作成功'
    status = 1
    data = {}

    def __init__(self, msg=None, code=None, status=None,data=None,
                 headers=None):
        if code:
            self.code = code
        if status:
            self.status = status
        if msg:
            self.msg = msg
        if data:
            self.data = data
        super(APIResponse, self).__init__(msg, None)

    def get_body(self, environ=None):
        body = dict(
            msg=self.msg,
            status=self.status,
            data = self.data
        )
        text = json.dumps(body)
        return text

    def get_headers(self, environ=None):
        """Get a list of headers."""
        return [('Content-Type', 'application/json')]

