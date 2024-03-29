import json
import hashlib
from datetime import datetime, timedelta

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.exc import IntegrityError

from passlib.apps import custom_app_context as pwd_context

db = SQLAlchemy()


class BaseFieldsMixin(object):
    id =            db.Column(db.Integer, primary_key=True)
    created_at =    db.Column(db.DateTime, default=datetime.utcnow)
    updated_at =    db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class BaseMethodsMixin(object):
    def to_dict(self):
        cols = {c.name: getattr(self, c.name) for c in self.__table__.columns}
        for k, v in cols.items():
            if isinstance(v, datetime):
                cols[k] = v.strftime("%Y-%m-%d %H:%M:%S")
        return cols

    def save(self):
        db.session.add(self)
        db.session.commit()
        return self

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return None


class BaseMixin(BaseFieldsMixin, BaseMethodsMixin):
    pass  # combine both mixins into simpler shorthand


# Actual models


class User(db.Model, BaseMixin):
    __tablename__ = "users"

    name =          db.Column(db.String(256))
    email =         db.Column(db.String(256), nullable=False, unique=True)
    password =      db.Column(db.String(256), nullable=False)

    last_seen_at =  db.Column(db.DateTime)
    is_admin =      db.Column(db.Boolean())

    password_reset_hash =   db.Column(db.String(32))
    password_reset_at =     db.Column(db.DateTime)

    def to_dict(self):
        d = super(User, self).to_dict()
        del d["password"]
        del d["password_reset_hash"]
        del d["password_reset_at"]
        return d

    def set_password(self, password):
        self.password = pwd_context.hash(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password)

    def gravatar_url(self, size=200):
        return "https://www.gravatar.com/avatar/{md5}?size={size}".format(
            md5=hashlib.md5(self.email.encode('utf-8')).hexdigest(),
            size=size
        )
