from datetime import UTC, datetime, timedelta
from functools import wraps
from random import randint

import requests
from flask import abort, current_app, flash, redirect, render_template, url_for
from flask_login import current_user
from flask_mailman import EmailMessage
from itsdangerous import URLSafeTimedSerializer
from jinja2 import TemplateNotFound
from sqlalchemy import select

from app import db
from app.models import CompletedChapter, CurrentChapter, User


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
        if current_user.is_authenticated and current_user.confirmation is True:
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


# NEW_FUNC: Make the sending of the email asynchrously
def send_confirmation_email(recipient):
    link = generate_link("register_routes.confirm_email", recipient)

    msg = EmailMessage(
        "Activación de cuenta",
        f"Para activar tu cuenta en Time Welsch, por favor sigue este link:\n{link}",
        current_app.config["MAIL_DEFAULT_SENDER"],
        [recipient],
    )

    Thread(
        target=send_async_email,
        args=[
            msg,
        ],
    ).start()


# NEW_FUNC: Implement the functionality that only the reset password link works one time
def send_reset_password_email(recipient):
    link = generate_link("login_routes.reset_password", recipient)

    msg = EmailMessage(
        "Reestablecer Contraseña",
        f"Para reestablecer tu contraseña en Time Welsch, por favor sigue este link:\n{link}",
        current_app.config["MAIL_DEFAULT_SENDER"],
        [recipient],
    )

    Thread(
        target=send_async_email,
        args=[
            msg,
        ],
    ).start()


def send_contact_me_email(name, contact_email, message):
    msg = EmailMessage(
        "Contacto realizado",
        f"Nombre: {name}\nCorreo: {contact_email}\nMensaje: {message}",
        current_app.config["MAIL_DEFAULT_SENDER"],
        [current_app.config["MAIL_CONTACT_ME_RECEIVER"]],
    )

    Thread(
        target=send_async_email,
        args=[
            msg,
        ],
    ).start()


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


# BUG: Sometimes it returns two objects with the same date and the next one jumps one day.
# It's not a big deal but when I design this function I want one chapter completed by day.
def generate_completed_date(date: datetime):
    new_date = datetime(
        year=date.year,
        month=date.month,
        day=date.day,
        hour=randint(0, 23),
        minute=randint(0, 59),
        second=randint(0, 59),
    )
    new_date += timedelta(days=1)

    return new_date


def get_unique_name(name):
    similar_users = db.session.scalars(
        select(User.username).where(User.username.like(f"{name}%"))
    ).all()

    if not similar_users:
        return f"{name}_1"

    numbers = [int(user.split("_")[-1]) for user in similar_users]
    max_number = max(numbers)
    new_number = max_number + 1

    prefix = similar_users[0].rsplit("_", 1)[0]
    return f"{prefix}_{new_number}"


# TODO: Create the logic to auto delete the demo users
def create_demo_user(current_chapter=1, name="usuario_demo"):
    # Find a unique name for the user
    username = get_unique_name(name)
    # create the user
    if current_chapter > 1:
        creation_date = datetime.now(UTC) - timedelta(days=current_chapter - 1)

        user = User(
            username=username,
            email=f"{username}@user.demo",
            password="12345678",
            date_created=creation_date,
            confirmation=True,
        )
    else:
        user = User(
            username=username,
            email=f"{username}@user.demo",
            password="12345678",
            confirmation=True,
        )

    db.session.add(user)
    db.session.commit()

    # Create the current_chapter for the new user
    current_chapter_model = CurrentChapter(
        user_id=user.id, current_chapter=current_chapter
    )

    db.session.add(current_chapter_model)
    db.session.commit()

    # Create the completed chapters for the new user
    completed_date = user.date_created

    for chapter_id in range(1, current_chapter):
        completed_date = generate_completed_date(completed_date)

        completed_chapter = CompletedChapter(
            user_id=user.id, chapter_id=chapter_id, completed_date=completed_date
        )
        db.session.add(completed_chapter)

    db.session.commit()

    return user
