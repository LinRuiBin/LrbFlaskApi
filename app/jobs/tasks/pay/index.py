'''
python3 job.py runjob -m pay/index
在linux部署环境 需要获取当前python3环境的绝对路径
还有虚拟环境
'''
from app.models.base import db
from app.models.order import *
from app.models.user import User
# from app.libs.scheduler import scheduler
from flask import current_app
import os

#这个是通过执行脚本调用
class JobTask():
    def __init__(self):
        pass
    def run(self,params):
        with current_app.app_context():
            user = User.query.filter_by(nickname='Super').first()
            if user:
                phone = int(user.phone)
                if phone < 18675079700:
                    phone += 1
                if phone == 18675079700:
                    phone -= 100
                user.phone = str(phone)
                db.session.add(user)
                db.session.commit()


#通过scheduler 装饰器调用
# @scheduler.task('interval', id='do_job_1', seconds=10, misfire_grace_time=900)
# def payJob():
#     with scheduler.app.app_context():
#         user = User.query.filter_by(nickname='Super').first()
#         if user:
#             phone = int(user.phone)
#             if phone < 18675079700:
#                 phone += 1
#             if phone == 18675079700:
#                 phone -= 100
#             user.phone = str(phone)
#             db.session.add(user)
#             db.session.commit()
#             print('自动执行任务完成')