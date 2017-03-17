import json
import hashlib
from datetime import datetime, timedelta

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.exc import IntegrityError

from passlib.apps import custom_app_context as pwd_context

db = SQLAlchemy()


class BaseMixin(object):
    id =            db.Column(db.Integer, primary_key=True)
    created_at =    db.Column(db.DateTime, default=datetime.utcnow)
    updated_at =    db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_json(self):
        cols = {c.name: getattr(self, c.name) for c in self.__table__.columns}
        for k, v in cols.items():
            if isinstance(v, datetime):
                cols[k] = v.strftime("%Y-%m-%d %H:%M:%S")
        return cols


class User(db.Model, BaseMixin):
    __tablename__ = "users"

    email =         db.Column(db.String(256), unique=True)
    password =      db.Column(db.String(256))
    is_admin =      db.Column(db.Boolean())

    def set_password(self, password):
        self.password = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password)

    def gravatar_url(self, size=200):
        return "https://www.gravatar.com/avatar/{md5}?size={size}".format(
            md5=hashlib.md5(self.email).hexdigest(),
            size=size
        )
