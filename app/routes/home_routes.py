from flask import (
    Blueprint,
    render_template,
    current_app,
    request,
    abort,
    redirect,
    url_for,
)
from app.forms import LoginForm, RegisterFrom
import requests
from app.models import User
from app import db
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select
from flask_mailman import EmailMessage

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


def generate_activation_link(recipient):
    serializer = current_app.config["SERIALIZER"]
    token = serializer.dumps(recipient, "email_confirmation")
    link = f"{request.host_url.rstrip('/')}{url_for("home_routes.confirm_email", token=token)}"
    return link


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

        activation_link = generate_activation_link(user.email)

        msg = EmailMessage(
            "Account Activation",
            f"To activate your account at Time Welsch, please follow this link:\n{activation_link}",
            current_app.config["MAIL_USERNAME"],
            [user.email],
        )

        msg.send()

        return render_template("confirmation.html")

    return render_template(
        "register.html", form=form, site_key=current_app.config["RECAPTCHA_PUBLIC_KEY"]
    )


@bp.get("/confirm_email/<token>")
def confirm_email(token):
    serializer = current_app.config["SERIALIZER"]
    email = None
    try:
        email = serializer.loads(token, salt="email_confirmation", max_age=60)
    except:
        # CHECK: If something went wrong with the confirmation. How can the user try again.
        # Because the user has already been saved to the db. maybe render a page with a link
        # to try again or if the user closed the page. When he tries to login send the
        # confirmation again
        return "Something went wrong with the confirmation try again"

    user = db.session.scalars(select(User).where(User.email == email)).one()
    user.confirmation = True
    db.session.commit

    return redirect(url_for("home_routes.login"))
