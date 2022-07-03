import os
import unittest

from flask_testing import TestCase
from flask import url_for

from app import app
from models import db

USER_PASSWORD = "foobar123"


class TestCase(TestCase):

    def setUp(self):
        db.create_all()

        self.user = User(name="Test User", email="test-user@example.com")
        self.user.set_password(USER_PASSWORD)
        self.user.save()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def create_app(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = os.environ["TEST_DATABASE_URL"]
        return app

    def check_url(self, url, status=200, flash=None):
        r = self.client.get(url)
        self.assertEqual(r.status_code, status)
        if flash:
            self.assertIn(flash, r.data)


class TestWeb(TestCase):

    def test_homepage(self):
        self.check_url("/")

    def test_signup(self):
        url = url_for("web.sign_up")
        self.check_url(url)

        form_data = {
            "name": self.user.name,
            "email": self.user.email,
            "password": USER_PASSWORD,
        }
        r = self.client.post(url, data=form_data, follow_redirects=True)
        self.assertMessageFlashed("Thanks for signing up!", "success")

    def test_login(self):
        url = url_for("web.login")
        self.check_url(url)

        form_data = {
            "email": self.user.email,
            "password": USER_PASSWORD,
        }
        r = self.client.post(url, data=form_data, follow_redirects=True)
        self.assertEqual(r.status_code, 200)

    def test_logout(self):
        self.check_url(url_for("web.logout"), status=302)

    def test_reset_email(self):
        self.check_url(url_for("web.reset_email"))

    def test_reset_password(self):
        pass


if __name__ == '__main__':
    unittest.main()