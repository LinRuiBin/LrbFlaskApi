"""
 Created by LRB on 2018/5/7.

"""

import requests,json
from flask import request, jsonify

from app.libs.error_code import ClientTypeError, Success,NodataReponse,SuccessReponse,FailReponse
from app.libs.redprint import Redprint
from app.models.user import User,OauthMemberBind
from app.validators.forms import ClientForm, UserEmailForm,WxClientForm
from app.libs.enums import ClientTypeEnum
from werkzeug.exceptions import HTTPException
from app import get_app
from app.models.base import db
from app.api.v1.token import generate_auth_token
from flask import current_app

__author__ = 'LRB'

api = Redprint('client')
app = current_app

@api.route('/register', methods=['POST'])
def create_client():

    form = ClientForm().validate_for_api()
    promise = {
        ClientTypeEnum.USER_EMAIL: __register_user_by_email
    }
    promise[form.type.data]()
    return Success()

#微信注册
@api.route('/wx_register', methods=['POST'])
def create_clent_wx():

    form = WxClientForm().validate_for_api() #验证
    # req = request.values
    req = request.get_json(silent=True)
    code = form.code.data
    wxopenId = OauthMemberBind.getWeChatOpenId(code)
    if not wxopenId:
      raise FailReponse(data=None,msg="微信注册失败")

    nickname = req['nickName'] if 'nickName' in req else ''
    sex = req['gender'] if 'gender' in req else 0
    avatar = req['avatarUrl'] if 'avatarUrl' in req else ''
    bind_info = OauthMemberBind.query.filter_by(openid=wxopenId, type=form.type.data.value).first()

    if not bind_info:
        wx_user = User()
        wx_user.nickname = nickname
        wx_user.gender = sex
        wx_user.avatar = avatar
        wx_user.auth = 1
        with db.auto_commit():
          db.session.add(wx_user)

        model_bind = OauthMemberBind()
        model_bind.user_id = wx_user.id
        model_bind.type = form.type.data.value  #200为微信登录
        model_bind.openid = wxopenId
        model_bind.client_type ='微信小程序'
        model_bind.extra = ''
        db.session.add(model_bind)
        with db.auto_commit():
          db.session.commit()

        bind_info = model_bind

    user_info = User.query.filter(User.id==bind_info.user_id).first()

    expiration = current_app.config['TOKEN_EXPIRATION']
    token = generate_auth_token(user_info.id ,
                                ClientTypeEnum(200) ,
                                user_info.scope ,
                                expiration)
    data = {}
    data["token"] = token.decode('ascii')
    data["userInfo"] = {"nickname": user_info.nickname , "avatar": user_info.avatar}
    return SuccessReponse(data=data,msg="登录成功")
    # res = {"code": 200 , "data": data , "msg": "登录成功"}
    # return jsonify(res)


def __register_user_by_email():
    form = UserEmailForm().validate_for_api()
    User.register_by_email(form.nickname.data,
                           form.account.data,
                           form.secret.data)



