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


@manager.command
def seed():
    u = User(email="test@example.com", is_admin=False)
    u.set_password("foobar123")

    db.session.add(u)
    db.session.commit()


@manager.option("-e", "--email", dest="email", default=None)
@manager.option("-p", "--pass", dest="password", default=None)
def admin(email, password):
    if not email or not password:
        return "Can't setup admin without email and password"

    u = User(email=email, is_admin=True)
    u.set_password(password)

    try:
        db.session.add(u)
        db.session.commit()

        return "Successfully added {} with that password".format(email)
    except IntegrityError:
        db.session.rollback()
        print "Admin with that email already exists, updating their password"

        u = User.query.filter_by(email=email).one()
        u.set_password(password)

        db.session.add(u)
        db.session.commit()

        return "Successfully updated the admin password for {}".format(email)


if __name__ == '__main__':
    manager.run()
