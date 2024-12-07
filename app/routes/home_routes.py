from flask import Blueprint, render_template, current_app, request, abort, redirect
from app.forms import LoginForm, RegisterFrom
import requests
from app.models import User
from app import db
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select

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
    form = RegisterFrom()

    if form.validate_on_submit():

        # TODO: Check the captcha score

        user = User(
            username=form.username.data,
            email=form.email.data,
            password=form.password.data,
        )

        db.session.add(user)

        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()

            existing_user = db.session.scalar(
                select(User)
                .where(
                    (User.username == form.username.data)
                    | (User.email == form.email.data)
                )
                .one()
            )

            if existing_user.username == form.username.data:
                form.username.errors.append("Este nombre de usuario ya esta en uso")
            if existing_user.email == form.email.data:
                form.email.errors.append("Una cuenta ya está usando este correo")

        # TODO: Create the logic to create the confirmation link and send the email with it

        return render_template("confirmation.html")

    return render_template(
        "register.html", form=form, site_key=current_app.config["RECAPTCHA_PUBLIC_KEY"]
    )
