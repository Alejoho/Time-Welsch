from flask import Blueprint, flash, render_template

from app.forms import ContactMeForm
from .complements import send_contact_me_email

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
    form = ContactMeForm()

    if form.validate_on_submit():
        send_contact_me_email(form.name.data, form.email.data, form.message.data)
        form.name.data = ""
        form.email.data = ""
        form.message.data = ""
        flash("Mensaje enviado", "success")

    return render_template("home/contact_me.html", form=form)
