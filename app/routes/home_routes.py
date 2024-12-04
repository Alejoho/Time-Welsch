from flask import Blueprint, render_template

bp = Blueprint("home_routes", __name__)


@bp.get("/")
def home():
    return render_template("test.html")
