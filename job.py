from flask_script import Manager
from app import app
# from app.libs.scheduler import scheduler
from app.jobs.launcher import runJob
import os

manager = Manager(app)

manager.add_command('runjob', runJob())

# 可以不使用scheduler  直接调用 python3 job.py runjob pay/index

if __name__ =='__main__':
    # if os.environ.get('WERKZEUG_RUN_MAIN') == 'true':  # 解决FLASK DEBUG模式定时任务执行两次
    #     scheduler.init_app(app)
    #     scheduler.start()
    manager.run()