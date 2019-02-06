from datetime import datetime

from functools import wraps
from flask import request, redirect, session, flash, url_for

from models import User

def login_required(f):
    @wraps(f)
    def func(*args, **kwargs):
        session["next_page"] = request.path
        if 'user_id' not in session or session['user_id'] is None:
            flash("You must be logged in to view that.", "error")
            return redirect(url_for("web.login"))
        request.user = User.query.filter_by(id=session['user_id']).first()

        request.user.last_seen_at = datetime.utcnow()
        request.user.save()

        if request.user.is_admin and request.args.get("m"):
            request.user = User.query.filter_by(id=request.args.get("m")).first()
        return f(*args, **kwargs)
    return func

