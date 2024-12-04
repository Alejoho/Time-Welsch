from flask import Blueprint, render_template

bp = Blueprint("home_routes", __name__)


@bp.get("/")
def home():
    return render_template("test.html")


@bp.get("/sobre_el_autor")
def about_author():
    return render_template("author.html")


@bp.get("/por_qué_este_libro")
def why_this_book():
    return render_template("why_this_book.html")
