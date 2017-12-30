from flask import Blueprint, render_template, request, redirect, session, flash, url_for

from models import db, IntegrityError, User

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

    u = User(email=request.form.get('email'))
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
