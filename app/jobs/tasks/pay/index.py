'''
python3 ginger.py runjob -m pay/index
'''
from app.models.base import db
from app.models.order import *
from app.models.user import User

class JobTask():
    def __init__(self):
        pass
    def run(self,params):
        print('运行任务')
        user = User.query.filter_by(nickname='Super').first()
        if user:
            phone = int(user.phone)
            phone += 1
            user.phone = str(phone)
            db.session.add(user)
            db.session.commit()

