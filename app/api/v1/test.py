from flask import jsonify, g

from app.libs.error_code import DeleteSuccess, AuthFailed,SuccessReponse
from app.libs.redprint import Redprint
from app.libs.token_auth import auth
from app.models.base import db
from app.celery.tasks import tetstCelery
from flask import session
from flask import request
from app import redis_db
from app import cache

api = Redprint('test')

@api.route('', methods=['GET','POST'])
# @cache.cached(timeout=60,key_prefix='cache_testkey')
def test():
  # print('no cache')
  cheest = 0
  cache = redis_db.get('test1')
  cheest = int(cache)+1 if cache else 0
  redis_db.set(name='test1',value=cheest)
  return SuccessReponse(msg=str(cheest))
