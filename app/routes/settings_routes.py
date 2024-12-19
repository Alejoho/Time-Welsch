from flask import Blueprint, render_template, redirect, url_for, flash
from app.forms import ChangePassword
from flask_login import current_user
from app import db

bp = Blueprint("settings_routes", __name__)


@bp.route("/cambiar-contrasena", methods=["GET", "POST"])
def change_password():
    form = ChangePassword()
    form.username.data = current_user.username

    if form.validate_on_submit():
        current_user.password = form.new_password.data
        db.session.commit()
        flash("Tu contraseña ha sido cambiada.", "success")
        return redirect(url_for("main_routes.my_route"))

    return render_template("register_login/change_password.html", form=form)
