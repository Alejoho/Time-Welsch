from flask import Blueprint, render_template
from app.forms import ChangePassword
from flask_login import current_user

bp = Blueprint("settings_routes", __name__)


@bp.route("/cambiar-contrasena", methods=["GET", "POST"])
def change_password():
    form = ChangePassword()
    form.username.data = current_user.username

    if form.validate_on_submit():
        return "passed the test"

    return render_template("register_login/change_password.html", form=form)
