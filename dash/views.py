from flask import Blueprint, render_template, request, redirect, session, flash, url_for, abort

from dash.utils import login_required

dash = Blueprint('dash', __name__, template_folder="dash")

@dash.route('/dashboard/', methods=['GET'])
@login_required
def dashboard():

    if False:
        return redirect(url_for(".some_other_view_function_name"))

    return render_template("root.html")
