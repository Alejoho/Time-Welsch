from functools import wraps
from flask import flash, redirect, render_template, url_for, current_app, abort
from flask_login import current_user
from itsdangerous import URLSafeTimedSerializer
from flask_mailman import EmailMessage
from jinja2 import TemplateNotFound
import requests


def redirect_authenticated_users(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if current_user.is_authenticated:
            flash("Tu sesión ya está iniciada", "info")
            return redirect(url_for("main_routes.my_route"))
        return func(*args, **kwargs)

    return decorated_function


def block_confirmed_users(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if current_user.confirmation is True:
            return abort(401)
        return func(*args, **kwargs)

    return decorated_function


def block_unconfirmed_users(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if current_user.confirmation is False:
            flash("Por favor confirma tu cuenta!", "warning")
            return redirect(url_for("register_routes.unconfirmed"))
        return func(*args, **kwargs)

    return decorated_function


def check_chapter(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        chapter_number = args[0] if args else kwargs.get("chapter_number")
        if chapter_number > current_user.current_chapter:
            flash("Faltan capítulos por leer.", "info")
            return redirect(url_for("main_routes.my_route"))
        return func(*args, **kwargs)

    return decorated_function


def verify_recaptcha(recaptcha_response):
    url = "https://www.google.com/recaptcha/api/siteverify"
    data = {
        "secret": current_app.config["RECAPTCHA_PRIVATE_KEY"],
        "response": recaptcha_response,
    }
    response = requests.post(url, data=data)
    result = response.json()

    return result["success"] and result["score"] >= 0.5


def generate_link(route, recipient):
    serializer = URLSafeTimedSerializer(current_app.config["SECRET_KEY"])
    token = serializer.dumps(
        recipient, salt=current_app.config["SECURITY_PASSWORD_SALT"]
    )
    link = url_for(route, token=token, _external=True)
    return link


def send_confirmation_email(recipient):
    link = generate_link("register_routes.confirm_email", recipient)

    msg = EmailMessage(
        "Activación de cuenta",
        f"Para activar tu cuenta en Time Welsch, por favor sigue este link:\n{link}",
        current_app.config["MAIL_USERNAME"],
        [recipient],
    )

    msg.send()


# LATER: Implement the functionality that only the reset password link works one time
def send_reset_password_email(recipient):
    link = generate_link("login_routes.reset_password", recipient)

    msg = EmailMessage(
        "Reestablecer Contraseña",
        f"Para reestablecer tu contraseña en Time Welsch, por favor sigue este link:\n{link}",
        current_app.config["MAIL_USERNAME"],
        [recipient],
    )

    msg.send()


def confirm_token(token, expiration):
    serializer = URLSafeTimedSerializer(current_app.config["SECRET_KEY"])
    email = serializer.loads(
        token, salt=current_app.config["SECURITY_PASSWORD_SALT"], max_age=expiration
    )

    return email


def handle_confirmation_error(message):
    flash(message, "danger")
    return render_template("register_routes.confirmation")


def handle_reset_password_error(message):
    flash(message, "danger")
    return redirect(url_for("login_routes.reset_password_request"))


def chapter_dont_exist(number):
    template_name = f"chapters/chapter_{number}.html"
    try:
        current_app.jinja_env.get_template(template_name)
        return False
    except TemplateNotFound:
        return True
