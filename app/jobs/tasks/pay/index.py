'''
python3 ginger.py runjob -m pay/index
'''
from app.models.base import db
from app.models.order import *
from app.models.user import User
from flask_apscheduler import APScheduler
from app.libs.scheduler import scheduler

#这个是通过执行脚本调用
class JobTask():
    def __init__(self):
        pass
    def run(self,params):
        print('运行任务')
        user = User.query.filter_by(nickname='Super').first()
        if user:
            phone = int(user.phone)
            if phone < 18675079600:
                phone += 1
            if phone > 18675079700:
                phone -= 10
            user.phone = str(phone)
            db.session.add(user)
            db.session.commit()


#通过scheduler 装饰器调用
@scheduler.task('interval', id='do_job_1', seconds=10, misfire_grace_time=900)
def payJob():
    with scheduler.app.app_context():
        user = User.query.filter_by(nickname='Super').first()
        if user:
            phone = int(user.phone)
            if phone < 18675079600:
                phone += 1
            if phone > 18675079700:
                phone -= 10
            user.phone = str(phone)
            db.session.add(user)
            db.session.commit()
            # print('自动执行任务完成')