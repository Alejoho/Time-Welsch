from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import login_required, current_user


bp = Blueprint("main_routes", __name__)


@bp.before_request
@login_required
def check_confirmed():
    if current_user.confirmation is False:
        flash("Por favor confirma tu cuenta!", "warning")
        return redirect(url_for("register_routes.unconfirmed"))


# TODO: Desing the route page with all the chapters and its descriptions. But only
# completely implement the two first chapters
@bp.get("/mi-ruta")
def my_route():
    return render_template("main/my_route.html")


@bp.get("/resumen")
def summary():
    return render_template("main/summary.html")


@bp.get("/ejercicios")
def exercises():
    return render_template("main/exercises.html")


@bp.get("/chapter/<number>")
def show_chapter(number):
    return render_template(f"chapters/chapter_{number}.html", number=int(number))
