from flask import jsonify, g
from flask import session
from flask import request

from app.libs.error_code import DeleteSuccess, AuthFailed, SuccessReponse
from app.libs.redprint import Redprint
from app.libs.token_auth import auth
from app.models.base import db
from app.celery.tasks import tetstCelery
from app import redis_db
from app import cache
from app import limiter
from app.models.user import *
from app.service.WeChatService import *

import requests

from app.libs.token_auth import auth

api = Redprint('test')

@api.route('', methods=['GET','POST'])
# @cache.cached(timeout=60,key_prefix='cache_testkey')  #不带参数
# @limiter.limit("1/day")
@cache.memoize(timeout=60) # 带参数
def test():
  print('no cache')
  cheest = 0
  cache = redis_db.get('test1')
  cheest = int(cache)+1 if cache else 0
  redis_db.set(name='test1',value=cheest)
  return SuccessReponse(msg=str(cheest))


@api.route('/limit', methods=['GET','POST'])
@limiter.limit("1/day",error_message='访问太频繁，请稍后再试')
def testlimit():
  return SuccessReponse(msg="测试限制")


@api.route('/formid', methods=['GET','POST'])
@auth.login_required
def testformid():
  current_userid = g.user.uid
  formid = ''
  if request.method == "GET":
    formid = redis_db.get(current_userid)
    return  SuccessReponse(data={'formid':formid})
  else:
    req = request.get_json(silent=True)
    formid = req['formid'] if 'formid' in req else ''
    if len(formid) > 0:
       redis_db.set(current_userid,value=formid)
    return SuccessReponse(msg='保存成功')


@api.route('/wxpush', methods=['GET','POST'])
@auth.login_required
def testWxPush():
  current_userid = g.user.uid
  user = User.query.filter_by(id=current_userid).first_or_404()
  oauthbind = user.oauthBind[0]
  openid = oauthbind.openid
  wechat = WeChatService()
  access_token = wechat.getAccessToken()
  formid = redis_db.get(current_userid)
  formid = formid.decode(encoding='utf-8')
  headers = {'Content-Type': 'application/json'}
  url = "https://api.weixin.qq.com/cgi-bin/message/wxopen/template/send?access_token=%s" % access_token
  params = {
    "touser": openid, #用户id
    "template_id": "K2NXK5gf-0GyX9nD36oV0Eg3Yy5vYjvTnjA6L4BSf8U",#模版id 需要在后台创建
    "page": "pages/ucenter/index",#需要进入的页面
    "form_id": formid,#从表单获取 也可以是支付的prepayId  每个id只能推送一次
    "data": {
      "keyword1": {
        "value": "测试小程序推送1"
      },
      "keyword2": {
        "value": "测试小程序推送2"
      },
      "keyword3": {
        "value": "测试小程序推送3"
      },
      "keyword4": {
        "value": "测试小程序推送4"
      },
      "keyword5": {
        "value": "测试小程序推送5"
      }
    }
  }

  r = requests.post(url=url, data=json.dumps(params).encode('utf-8'), headers=headers)
  r.encoding = "utf-8"
  return SuccessReponse(msg='测试推送')