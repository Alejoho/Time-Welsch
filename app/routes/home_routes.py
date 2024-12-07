from flask import Blueprint, render_template, current_app, request, abort, redirect
from app.forms import LoginForm, RegisterFrom
import requests
from app.models import User

bp = Blueprint("home_routes", __name__)


@bp.get("/")
def index():
    return render_template("index.html")


@bp.get("/sobre_el_autor")
def about_author():
    return render_template("about_author.html")


@bp.get("/por_qué_este_libro")
def why_this_book():
    return render_template("why_this_book.html")


@bp.route("/contáctame", methods=["GET", "POST"])
def contact_me():
    return render_template("contact_me.html")


def verify_recaptcha(recaptcha_response):
    url = "https://www.google.com/recaptcha/api/siteverify"
    data = {
        "secret": current_app.config["RECAPTCHA_PRIVATE_KEY"],
        "response": recaptcha_response,
    }
    response = requests.post(url, data=data)
    result = response.json()

    return result["success"] and result["score"] >= 0.5


@bp.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        form.username.data = ""
        password = form.password.data
        form.password.data = ""
        recaptcha_response = request.form.get("g-recaptcha-response")

        if not verify_recaptcha(recaptcha_response):
            return abort(401)

        # TODO: Make the logic to login a user with the flask_login package

        print("The user is logged in!!!")
        return redirect("index")

    return render_template(
        "login.html", form=form, site_key=current_app.config["RECAPTCHA_PUBLIC_KEY"]
    )


@bp.route("/register", methods=["GET", "POST"])
def register():
    # TODO: Complete the logic to register a user
    form = RegisterFrom()

    if form.validate_on_submit():

        return render_template("confirmation.html")

    return render_template(
        "register.html", form=form, site_key=current_app.config["RECAPTCHA_PUBLIC_KEY"]
    )
