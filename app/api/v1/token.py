"""
 Created by LRB on 2018/5/7.

"""
from flask import current_app, jsonify

from app.libs.enums import ClientTypeEnum
from app.libs.error_code import AuthFailed,DataFail
from app.libs.redprint import Redprint
from app.models.user import User,OauthMemberBind
from app.validators.forms import ClientForm, TokenForm,WxClientForm
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, SignatureExpired, \
    BadSignature

api = Redprint('token')

__author__ = 'LRB'

@api.route('', methods=['POST'])
def get_token():
    form = ClientForm().validate_for_api()
    promise = {
        ClientTypeEnum.USER_EMAIL: User.verify,
    }
    identity = promise[ClientTypeEnum(form.type.data)](
        form.account.data,
        form.secret.data
    )
    # Token
    expiration = current_app.config['TOKEN_EXPIRATION']
    token = generate_auth_token(identity['uid'],
                                form.type.data,
                                identity['scope'],
                                expiration)
    t = {
        'token': token.decode('ascii')
    }
    return jsonify(t), 201

@api.route('/wx_login', methods=['POST'])
def get_wxtoken():
    form = WxClientForm().validate_for_api()
    code = form.code.data
    wxopenId = OauthMemberBind.getWeChatOpenId(code)
    if not wxopenId:
        raise AuthFailed(msg="微信登录失败")
    bind_info = OauthMemberBind.query.filter_by(openid=wxopenId , type=form.type.data.value).first()
    if not bind_info:
        raise AuthFailed(msg="尚未授权登录")
    # Token
    user_info = User.query.filter(User.id == bind_info.user_id).first()
    if not user_info:
        raise AuthFailed(msg="尚未授权登录")

    expiration = current_app.config['TOKEN_EXPIRATION']
    token = generate_auth_token(user_info.id ,
                                ClientTypeEnum(200) ,
                                user_info.scope ,
                                expiration)
    t = {
        'token': token.decode('ascii')
    }
    return jsonify(t), 201


@api.route('/secret', methods=['POST'])
def get_token_info():
    """获取令牌信息"""
    form = TokenForm().validate_for_api()
    s = Serializer(current_app.config['SECRET_KEY'])
    try:
        data = s.loads(form.token.data, return_header=True)
    except SignatureExpired:
        raise AuthFailed(msg='token is expired', error_code=1003)
    except BadSignature:
        raise AuthFailed(msg='token is invalid', error_code=1002)

    r = {
        'scope': data[0]['scope'],
        'create_at': data[1]['iat'],
        'expire_in': data[1]['exp'],
        'uid': data[0]['uid']
    }
    return jsonify(r)


def generate_auth_token(uid, ac_type, scope=None,
                        expiration=7200):
    """生成令牌"""
    s = Serializer(current_app.config['SECRET_KEY'],
                   expires_in=expiration)
    return s.dumps({
        'uid': uid,
        'type': ac_type.value,
        'scope':scope
    })
