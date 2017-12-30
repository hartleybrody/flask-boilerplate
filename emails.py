import os

import requests
from flask import render_template


class BaseEmail(object):

    send_from = "admin@example.com"
    translate_newlines = True

    def __init__(self, send_to, context):

        # make sure the context contains all the info we'll need to render this
        # better to fail early than have blank or malformed emails going out
        for key in self.required_context:
            if key not in context.keys():
                raise Exception("Cannot send email without the '{}'. {}".format(key, context))
            if not context[key]:
                raise Exception("Cannot send email with a blank '{}'. {}".format(key, context))


        html = render_template(self.template_path, **context)
        if self.translate_newlines:
            html = html.replace("\n", "<br>\n")

        return self.send(
            send_to,
            self.send_from,
            self.get_subject(**context),
            html
        )

    def get_subject(self):
        return NotImplementedError("Subclasses must define their own subject methods")

    def send(self, send_to, send_from, subject, html):
        print subject
        print html
        endpoint = "https://api.mailgun.net/v3/{domain}/messages".format(domain=os.environ["MAILGUN_DOMAIN"])
        r = requests.post(
            endpoint,
            auth=('api', os.environ["MAILGUN_API_KEY"]),
            data={
                "from": send_from,
                "to": send_to,
                "subject": subject,
                "html": html,
            }
        )


class WelcomeEmail(BaseEmail):

    required_context = ["user"]
    template_path = "email/welcome.html"

    def get_subject(self, user, **kwargs):  # non-used context keys can be swallowed w **kwargs
        return "Welcome, {}".format(user.email)


class PasswordResetEmail(BaseEmail):

    required_context = ["user"]
    template_path = "email/password-reset.html"

    def get_subject(self, **kwargs):  # non-used context keys can be swallowed w **kwargs
        return "Your password reset link"
