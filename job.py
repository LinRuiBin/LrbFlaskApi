from flask_script import Manager
from app import app
from app.jobs.launcher import runJob

manager = Manager(app)

manager.add_command('runjob', runJob())

if __name__ =='__main__':
    manager.run()