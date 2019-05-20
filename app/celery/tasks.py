"""
celery -A app.celery worker
"""

from app import celery
from app.models.base import db
from app.models.user import User
# from app import app
import time

@celery.task
def tetstCelery():
    print('执行异步任务')
    # with app.app_context():
    # time.sleep(20)
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
        print('执行完成')

