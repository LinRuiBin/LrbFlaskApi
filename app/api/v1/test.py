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