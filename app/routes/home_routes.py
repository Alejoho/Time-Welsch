from flask import Blueprint, render_template


bp = Blueprint("home_routes", __name__)


@bp.get("/")
def index():
    return render_template("home/index.html")


@bp.get("/sobre_el_autor")
def about_author():
    return render_template("home/about_author.html")


@bp.get("/por_qué_este_libro")
def why_this_book():
    return render_template("home/why_this_book.html")


@bp.route("/contáctame", methods=["GET", "POST"])
def contact_me():
    return render_template("home/contact_me.html")


@bp.get("/test-modal")
def test_modal():
    return render_template("test.html")
