from flask import (
    Blueprint,
    render_template,
    current_app,
    request,
    abort,
    redirect,
    url_for,
    flash,
)
from app.forms import LoginForm, RegisterFrom
import requests
from app.models import User
from app import db
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select
from flask_mailman import EmailMessage
from flask_login import login_user, login_required, current_user
from itsdangerous import URLSafeTimedSerializer
from .complements import check_confirmed, confirm_token, send_confirmation_email

bp = Blueprint("home_routes", __name__)


# TODO: Change all the endpoints to spanish
@bp.get("/")
@login_required
# CHECK: This decorator
@check_confirmed
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
        recaptcha_response = request.form.get("g-recaptcha-response")

        if not verify_recaptcha(recaptcha_response):
            return abort(401)

        user = db.session.scalars(
            select(User).where(User.username == form.username.data)
        ).first()

        login_user(user)
        return redirect(url_for("home_routes.index"))

    return render_template(
        "login.html", form=form, site_key=current_app.config["RECAPTCHA_PUBLIC_KEY"]
    )


# TODO: avoid reseting the passwords fields when submiting the form
@bp.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterFrom()

    if form.validate_on_submit():
        recaptcha_response = request.form.get("g-recaptcha-response")

        if not verify_recaptcha(recaptcha_response):
            return abort(401)

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

            existing_user = db.session.scalars(
                select(User).where(
                    (User.username == form.username.data)
                    | (User.email == form.email.data)
                )
            ).one_or_none()

            if existing_user.username == form.username.data:
                form.username.errors.append("Este nombre de usuario ya esta en uso")
            if existing_user.email == form.email.data:
                form.email.errors.append("Una cuenta ya está usando este correo")

        send_confirmation_email(user.email)

        login_user(user)

        return redirect(url_for("home_routes.confirmation"))

    return render_template(
        "register.html", form=form, site_key=current_app.config["RECAPTCHA_PUBLIC_KEY"]
    )


@bp.get("/confirm_email/<token>")
@login_required
def confirm_email(token):
    try:
        email = confirm_token(token)
    except:
        # CHECK: This logic if something went wrong
        flash(
            "The confirmation link you have tried is invalid or has expired.", "danger"
        )
        return redirect(url_for("home_routes.resend_confirmation"))

    if current_user.confirmed:
        flash("Account already confirmed.", "success")
    else:
        current_user.confirmation = True
        db.session.commit()
        flash("You have confirmed your account.", "success")
    return redirect(url_for("home_routes.index"))


@bp.get("/resend-confirmation")
@login_required
def resend_confirmation():
    send_confirmation_email(current_user.email)
    flash("A new confirmation email has been sent.", "success")
    return redirect(url_for("home_routes.confirmation"))


@bp.route("/unconfirmed")
@login_required
def unconfirmed():
    if current_user.confirmation:
        return redirect(url_for("home_routes.index"))
    flash("Please confirm your account!", "warning")
    return render_template("confirmation.html")


# just for testing. delete later on
@bp.get("/confirmacion")
def confirmation():
    return render_template("confirmation.html")
