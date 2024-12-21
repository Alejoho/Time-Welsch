from flask import Blueprint, render_template, redirect, request, url_for, flash
from app.forms import ChangePasswordForm
from flask_login import current_user, login_required, logout_user
from app import db
from .complements import block_unconfirmed_users

bp = Blueprint("settings_routes", __name__)


@bp.before_request
@login_required
@block_unconfirmed_users
# This is just a function to avoid and error
def bypass_error():
    pass


@bp.route("/cambiar-contrasena", methods=["GET", "POST"])
def change_password():
    form = ChangePasswordForm()
    form.username.data = current_user.username

    if form.validate_on_submit():
        current_user.password = form.new_password.data
        db.session.commit()
        flash("Tu contraseña ha sido cambiada.", "success")
        return redirect(url_for("main_routes.my_route"))

    return render_template("account_managment/change_password.html", form=form)


@bp.post("/eliminar_cuenta")
def delete_account():
    if request.form.get("username") == current_user.username:

        db.session.delete(current_user)

        db.session.commit()

        logout_user()
        flash("Cuenta eliminada.", "success")
        return redirect(url_for("login_routes.login"))
    flash("No se pudo eliminar la cuenta. No introdujo el usuario correcto.", "danger")
    return redirect(url_for("main_routes.my_route"))
