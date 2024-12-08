from flask import Blueprint, render_template
from flask_login import login_required
from .complements import check_confirmed


bp = Blueprint("main_routes", __name__)


# TODO: Look up if is there a way to aply a decorator to a whole blueprint
@bp.get("/mi-ruta")
# FIXME: Fix the flash message of the login required decorator
@login_required
@check_confirmed
def my_route():
    return render_template("main/my_route.html")


@bp.get("/resumen")
@login_required
@check_confirmed
def summary():
    return render_template("main/summary.html")


@bp.get("/ejercicios")
@login_required
@check_confirmed
def exercises():
    return render_template("main/exercises.html")
