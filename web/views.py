import random
from datetime import datetime, timedelta

from flask import Blueprint, render_template, request, redirect, session, flash, url_for

from models import db, IntegrityError, User
from emails import WelcomeEmail, PasswordResetEmail

web = Blueprint('web', __name__)

@web.route('/', methods=['GET'])
def homepage():
    return render_template("web/homepage.html")


@web.route('/sign-up/', methods=['GET', 'POST'])
def sign_up():

    if session.get('user_id'):
        flash("You're already logged in", "success")
        return redirect(url_for("dash.root"))

    if request.method == 'GET':
        return render_template("web/sign-up.html")

    u = User(
        name=request.form.get('name'),
        email=request.form.get('email'),
        is_admin=False
    )
    u.set_password(request.form.get('password'))
    try:
        db.session.add(u)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        flash("Looks like you've already signed up. Try logging in.", "error")
        return redirect(url_for("web.login"))

    flash("Thanks for signing up!", "success")
    session['user_id'] = u.id

    # WelcomeEmail(u.email, dict(user=u))

    return redirect(url_for("dash.root", signup=1))


@web.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        if session.get('user_id'):
            flash("You're already logged in", "success")
            return redirect(url_for("dash.root"))
        return render_template("web/login.html")

    u = User.query.filter_by(email=request.form.get("email")).first()
    if not u:
        flash("No user with that email address", "error")
        return redirect(url_for("web.login"))

    if not u.verify_password(request.form.get("password")):
        flash("Incorrect password", "error")
        return redirect(url_for("web.login"))

    session['user_id'] = u.id

    if "next_page" in session:
        next_page = session["next_page"]
        del session["next_page"]
        return redirect(next_page)

    return redirect(url_for("dash.root"))


@web.route('/logout/', methods=['GET'])
def logout():
    try:
        del session['user_id']
    except KeyError:
        pass
    return redirect(url_for("web.homepage"))


@web.route('/reset/email/', methods=['GET', 'POST'])
def reset_email():
    # step 1 of password reset, provide email address

    if request.method == "GET":
        return render_template("web/reset-email.html")

    email = request.form.get("email")
    user = User.query.filter_by(email=email).first()

    if not user:
        flash("No user with that email address", "error")
        return redirect(url_for("web.reset_email"))

    user.password_reset_hash = hex(random.getrandbits(128))[2:-1]
    user.password_reset_at = datetime.utcnow()

    db.session.add(user)
    db.session.commit()

    PasswordResetEmail(user.email, dict(user=user))

    flash("A password reset email has been sent to that address", "success")
    return redirect(url_for("web.reset_email"))


@web.route('/reset/password/', methods=['GET', 'POST'])
def reset_password():
    # step 2 of password reset, click link in email

    reset_hash = request.args.get("hash")
    cutoff = datetime.utcnow() - timedelta(hours=24)  # link is valid for 24 hours

    user = User.query.filter_by(password_reset_hash=reset_hash).filter(User.password_reset_at > cutoff).first()

    if not user:
        flash("Invalid reset token, please try again", "error")
        return redirect(url_for("web.reset_email"))

    if request.method == "GET":
        return render_template("web/reset-password.html", user=user)

    password = request.form.get("password")

    if not password == request.form.get("confirm_password"):
        flash("Those passwords didn't match", "error")
        return redirect(url_for("web.reset_password", hash=request.args.get("hash")))

    user.set_password(password)
    user.password_reset_hash = None
    user.password_reset_at = None

    db.session.add(user)
    db.session.commit()

    flash("Successfully updated your password", "success")
    return redirect(url_for("web.login"))


@web.route('/_ping/', methods=['GET'])
def ping():

    from cache import redis
    redis.set("ping-test", "ok")

    db.session.execute("SELECT 1")

    return redis.get("ping-test")

@web.route('/_exception/', methods=['GET'])
def exception():
    raise Exception("You want an exception? You got one!")