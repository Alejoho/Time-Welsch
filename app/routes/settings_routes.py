from flask import Blueprint, render_template, redirect, url_for, flash
from app.forms import ChangePassword
from flask_login import current_user, login_required, logout_user
from app import db
from sqlalchemy import select
from app.models import User

bp = Blueprint("settings_routes", __name__)


@bp.before_request
@login_required
# LATER: Convert this into a decorator. Called "confirmed_required"
def check_confirmed():
    if current_user.confirmation is False:
        flash("Por favor confirma tu cuenta!", "warning")
        return redirect(url_for("register_routes.unconfirmed"))


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


@bp.route("/eliminar-cuenta", methods=["GET"])
def delete_account():
    # CHECK: If this is the correct way to delete a user
    db.session.delete(current_user)

    db.session.commit()

    logout_user()

    return redirect(url_for("login_routes.login"))
