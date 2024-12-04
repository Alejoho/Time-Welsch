from flask import Blueprint

bp = Blueprint("home_routes", __name__)


@bp.get("/")
def home():
    return "Hello World"
