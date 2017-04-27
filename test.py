import os
import unittest

from flask_testing import TestCase

from app import app
from models import db


class TestCase(TestCase):

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def create_app(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = os.environ["TEST_DATABASE_URL"]
        return app

    def test_homepage(self):
        r = self.client.get('/')
        assert r.status_code == 200

    def test_signup_success(self):
        r = self.client.get("/sign-up/")
        assert r.status_code == 200

        r = self.client.post("/sign-up/", data={
            "email": "admin@example.com",
            "password": "foobar123",
        }, follow_redirects=True)
        assert "Thanks for signing up" in r.data


if __name__ == '__main__':
    unittest.main()