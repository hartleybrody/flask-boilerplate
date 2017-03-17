import os
import json
from datetime import datetime, timedelta
from collections import defaultdict

from flask import Flask
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from models import db, User

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ["DATABASE_URL"]
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)


@manager.option("-n", "--name", dest="name", default="Undefined")
def job(name):
    print "Running custom job: {}".format(name)


if __name__ == '__main__':
    manager.run()
