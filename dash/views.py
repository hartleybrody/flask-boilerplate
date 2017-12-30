import json

from flask import Blueprint, render_template, request, redirect, session, flash, url_for, abort

from dash.utils import login_required
from models import User

dash = Blueprint('dash', __name__)

@dash.route('/dashboard/', methods=['GET'])
@login_required
def root():

    if False:
        return redirect(url_for(".some_other_view_function_name"))

    js_init = {
        "users": [u.to_dict() for u in User.query.all()]
    }

    return render_template("dash/root.html", js_init=json.dumps(js_init))
