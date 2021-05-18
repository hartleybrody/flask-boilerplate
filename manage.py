import os
import json
from datetime import datetime, timedelta
from collections import defaultdict

import click
from app import app
from models import db, User, IntegrityError

@app.cli.command("job")
@click.option("-n", "--name", default="Undefined")
def job(name):
    """
    A basic job to show syntax.
    """
    print("Running custom job: {}".format(name))


@app.cli.command("seed")
def seed():
    """
    Setup an initially empty database with useful data.
    """
    u = User(email="test@example.com", is_admin=False)
    u.set_password("foobar123")

    db.session.add(u)
    db.session.commit()


@app.cli.command("admin")
@click.option("-e", "--email", default=None)
@click.option("-p", "--pass", default=None)
def admin(email, password):
    """
    Create an admin user.
    """
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
        print("Admin with that email already exists, updating their password")

        u = User.query.filter_by(email=email).one()
        u.set_password(password)

        db.session.add(u)
        db.session.commit()

        return "Successfully updated the admin password for {}".format(email)


if __name__ == '__main__':
    manager.run()
