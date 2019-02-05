import os

from flask import Flask, render_template
from raven.contrib.flask import Sentry
from flask_session import Session

from models import db
from web.views import web as web_blueprint
from dash.views import dash as dash_blueprint

app = Flask(__name__)
app.secret_key = '3n13m3@n13myn13m0-{{APP_SLUG}}'
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ["DATABASE_URL"]
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# secure the session cookies
app.config['SESSION_COOKIE_SECURE'] = True
app.config['SESSION_COOKIE_HTTPONLY'] = True

if os.environ.get("REDIS_URL"):
    from cache import redis_connection
    app.config['SESSION_TYPE'] = 'redis'
    app.config['SESSION_REDIS'] = redis_connection
    sess = Session()
    sess.init_app(app)

if os.environ.get("SENTRY_DSN"):
    sentry = Sentry(app, dsn=os.environ["SENTRY_DSN"])

app.register_blueprint(web_blueprint)
app.register_blueprint(dash_blueprint)

# add a timestamp-based cache buster to static files
static_last_update = 0
for directory in os.walk("static/"):
    file_names = directory[2]
    for file_name in file_names:
        if file_name.startswith("."):
            continue  # ignore config files
        ext = file_name.split(".")[-1]
        if ext not in ["css", "js"]:
            continue  # skip fonts and images
        file_path = os.path.join(directory[0], file_name)
        updated_at = os.path.getmtime(file_path)
        if updated_at > static_last_update:
            static_last_update = updated_at
app.config['static_last_update'] = str(int(static_last_update))[-6:]


@app.errorhandler(404)
def not_found(e):
    return render_template("404.html"), 404

@app.errorhandler(500)
def server_error(e):
    return render_template("500.html"), 500

@app.after_request
def apply_security_headers(response):

    # don't allow the site to load in an iframe (prevents click jacking)
    response.headers["X-Frame-Options"] = "DENY"

    # don't allow browsers to auto-detect mime type
    # they should trust the `Content-Type` header with each response
    response.headers["X-Content-Type-Options"] = "nosniff"

    return response

db.init_app(app)


if __name__ == '__main__':
    app.run(debug=True)

    # to run your local development server over SSL (recommened for finding content issues)
    # https://blog.filippo.io/mkcert-valid-https-certificates-for-localhost/
    # app.run(debug=True, ssl_context=(os.environ["LOCAL_SSL_CERT_PATH"], os.environ["LOCAL_SSL_KEY_PATH"]))
