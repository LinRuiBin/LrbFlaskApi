'''

导入需要更新的表对应的数据模型 否则不会更新
运行 dbmigrate.py
执行
python dbmigrate.py db init
python dbmigrate.py db migrate
python dbmigrate.py db upgrade

'''
from flask_script import Manager
from app import app
import app_register
from flask_migrate import Migrate,MigrateCommand
from app.models.base import db
# 必须导入需要更新的模型
from app.models import base,user, goods, adress,shopCart,order

manager = Manager(app)
# init  migrate upgrade
# 模型 -> 迁移文件 -> 表
# 1.要使用flask_migrate,必须绑定app和DB
migrate = Migrate(app, db)

# 2.把migrateCommand命令添加到manager中。
manager.add_command('db',MigrateCommand)

if __name__ =='__main__':
    manager.run()