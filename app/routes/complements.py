# app/routes/complements.py

from datetime import UTC, datetime, timedelta
from random import randint

import requests
from flask import current_app, flash, redirect, render_template, url_for
from flask_mailman import EmailMessage
from itsdangerous import URLSafeTimedSerializer
from jinja2 import TemplateNotFound
from sqlalchemy import select

from app import db
from app.models import CompletedChapter, CurrentChapter, User


def verify_recaptcha(recaptcha_response: str) -> bool:
    """
    Verifies if a reCaptcha response passes the need conditions to be valid.

    :param str recaptcha_response: The reCaptcha response
    :return bool: Returns True if it's valid, otherwise false
    """
    url = "https://www.google.com/recaptcha/api/siteverify"
    data = {
        "secret": current_app.config["RECAPTCHA_PRIVATE_KEY"],
        "response": recaptcha_response,
    }
    response = requests.post(url, data=data)
    result = response.json()

    return result["success"] and result["score"] >= 0.5


def generate_link(route: str, recipient: str) -> str:
    """
    Generates a link for a certain route with an email serialized as token in it.

    :param str route: The name of the route.
    :param str recipient: The email to serialize.
    :return str: Returns a link to the route with the email serialized as a token.
    """
    serializer = URLSafeTimedSerializer(current_app.config["SECRET_KEY"])
    token = serializer.dumps(
        recipient, salt=current_app.config["SECURITY_PASSWORD_SALT"]
    )
    link = url_for(route, token=token, _external=True)
    return link


# NEW_FUNC: Make the sending of the email asynchrously
def send_confirmation_email(recipient: str) -> None:
    """
    Sends an email to confirm the registration of an account.

    :param str recipient: The email with which the account was registered.
    """
    link = generate_link("register_routes.confirm_email", recipient)

    msg = EmailMessage(
        "Activación de cuenta",
        f"Para activar tu cuenta en Time Welsch, por favor sigue este link:\n{link}",
        current_app.config["MAIL_DEFAULT_SENDER"],
        [recipient],
    )

    msg.send()


# NEW_FUNC: Implement the functionality that only the reset password link works one time
def send_reset_password_email(recipient: str) -> None:
    """
    Sends an email to reset the password of an account.

    :param str recipient: The email of the account.
    """
    link = generate_link("login_routes.reset_password", recipient)

    msg = EmailMessage(
        "Reestablecer Contraseña",
        f"Para reestablecer tu contraseña en Time Welsch, por favor sigue este link:\n{link}",
        current_app.config["MAIL_DEFAULT_SENDER"],
        [recipient],
    )

    msg.send()


def send_contact_me_email(name: str, contact_email: str, message: str) -> None:
    """
    Sends a contact email to the owner of the web app.

    :param str name: The name of the person.
    :param str contact_email: The email of the person.
    :param str message: The message to send.
    """
    msg = EmailMessage(
        "Contacto realizado",
        f"Nombre: {name}\nCorreo: {contact_email}\nMensaje: {message}",
        current_app.config["MAIL_DEFAULT_SENDER"],
        current_app.config["MAIL_CONTACT_ME_RECEIVER"],
    )

    msg.send()


def confirm_token(token: str, expiration: int) -> str:
    """
    Deserialize a token and returns its content.

    :param str token: The token with the serialized email.
    :param int expiration: The expiration time of the token.
    :return str: Returns the deserialized email.
    """
    serializer = URLSafeTimedSerializer(current_app.config["SECRET_KEY"])
    email = serializer.loads(
        token, salt=current_app.config["SECURITY_PASSWORD_SALT"], max_age=expiration
    )

    return email


def handle_confirmation_error(message: str) -> str:
    """
    Renders a page with a message when the confirmation token is not valid for some reason.

    :param str message: The message to show with the reason.
    :return str: The rendered page.
    """
    flash(message, "danger")
    return render_template("register_routes.confirmation")


def handle_reset_password_error(message: str) -> str:
    """
    Renders a page with a message when the confirmation token is not valid for some reason.

    :param str message: The message to show with the reason.
    :return str: The rendered page.
    """
    flash(message, "danger")
    return redirect(url_for("login_routes.reset_password_request"))


def chapter_dont_exist(number: int) -> bool:
    """
    Determines if a chapter don't exist.

    :param int number: The chapter number.
    :return bool: Returns True if the chapter don't exist, otherwise false.
    """
    template_name = f"chapters/chapter_{number}.html"
    try:
        current_app.jinja_env.get_template(template_name)
        return False
    except TemplateNotFound:
        return True


# BUG: Sometimes it returns two objects with the same date and the next one jumps one day.
# It's not a big deal but when I design this function I want one chapter completed by day.
def generate_next_datetime(date: datetime) -> datetime:
    """Generates a datetime with a day(more or less) of difference with the passed date as parameter.

    :param datetime date: The previous datetime.
    :return datetime: Returns a datetime with a day of difference.
    """
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


def get_unique_name(name: str) -> str:
    """Generates a unique username based of the names previously store in the db.

    :param str name: The template name.
    :return str: Returns the unique name.
    """
    similar_users = db.session.scalars(
        select(User.username).where(User.username.like(f"{name}%"))
    ).all()

    if not similar_users:
        return f"{name}_1"

    # Gets the max number at the end of the user and adds one to it.
    numbers = [int(user.split("_")[-1]) for user in similar_users]
    max_number = max(numbers)
    new_number = max_number + 1

    # Creates a new name with the number
    prefix = similar_users[0].rsplit("_", 1)[0]
    return f"{prefix}_{new_number}"


def create_demo_user(current_chapter: int = 1, name: str = "usuario_demo") -> User:
    """Creates a demo user with all the needed data.

    :param int current_chapter: The current chapter the user is in, defaults to 1.
    :param str name: The user name, defaults to "usuario_demo".
    :return User: Returns the new User object.
    """
    username = get_unique_name(name)
    # Creates and stores the new user
    if current_chapter > 1:
        creation_date = datetime.now(UTC) - timedelta(days=current_chapter - 1)

        user = User(
            username=username,
            email=f"{username}@user.demo",
            password="12345678",
            date_created=creation_date,
            confirmation=True,
            is_demo=True,
        )
    else:
        user = User(
            username=username,
            email=f"{username}@user.demo",
            password="12345678",
            confirmation=True,
            is_demo=True,
        )

    db.session.add(user)
    db.session.commit()

    # Creates and stores the current_chapter for the new user
    current_chapter_model = CurrentChapter(
        user_id=user.id, current_chapter=current_chapter
    )

    db.session.add(current_chapter_model)
    db.session.commit()

    # Creates and stores the completed chapters for the new user
    completed_date = user.date_created

    for chapter_id in range(1, current_chapter):
        completed_date = generate_next_datetime(completed_date)

        completed_chapter = CompletedChapter(
            user_id=user.id, chapter_id=chapter_id, completed_date=completed_date
        )
        db.session.add(completed_chapter)

    db.session.commit()

    return user
