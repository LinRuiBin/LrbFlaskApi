from flask import jsonify, g

from app.libs.error_code import DeleteSuccess, AuthFailed,SuccessReponse
from app.libs.redprint import Redprint
from app.libs.token_auth import auth
from app.models.base import db
from app.celery.tasks import tetstCelery

api = Redprint('test')

@api.route('', methods=['GET','POST'])
def test():
    tetstCelery.delay()
    return SuccessReponse()