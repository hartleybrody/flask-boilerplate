from flask import Blueprint, render_template, request, redirect, session, flash, url_for, abort

from app.utils import login_required

app = Blueprint('app', __name__)

@app.route('/dashboard/', methods=['GET'])
@login_required
def dashboard():
    if not request.user.access_token:

        return render_template("dashboard/welcome.html")

    if request.user.stats:
        return redirect(url_for(".dashboard_leaderboard"))

    return redirect(url_for(".dashboard_form"))