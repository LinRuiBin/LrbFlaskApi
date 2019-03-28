"""
 Created by LRB on 2018/5/12.
"""
from flask import request
from wtforms import Form

from app.libs.error_code import ParameterException

__author__ = 'LRB'


class BaseForm(Form):
    def __init__(self):
        req = request
        data = request.get_json(silent=True)
        args = request.args.to_dict() #获取get 请求参数
        args = request.values.to_dict() if not args else {} #获取所有请求参数
        super(BaseForm, self).__init__(data=data, **args)

    def validate_for_api(self):
        valid = super(BaseForm, self).validate()
        if not valid:
            # form errors
            raise ParameterException(msg=self.errors)
        return self
