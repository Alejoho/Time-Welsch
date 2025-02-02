# app/forms/custom_validators.py

import requests
from flask import current_app
from sqlalchemy import select
from wtforms.validators import ValidationError

from app import db
from app.models import User


class EmailExistence(object):
    """Validates that the email address really exists and it can receive emails."""

    def __init__(self, message: str | None = None):
        if not message:
            message = "Email doesn't exist"
        self.message = message

    def __call__(self, form, field):
        if field.errors:
            return
        url = f'https://api.hunter.io/v2/email-verifier?email={field.data}&api_key={current_app.config["HUNTER_API_KEY"]}'
        try:
            response = requests.get(url)
        except:
            raise ValidationError("Verificación de correo fallida")

        if response.status_code != 200:
            raise ValidationError("Verificación de correo fallida. Inténtalo de nuevo")

        data = response.json()

        status = data.get("data", {}).get("status")
        result = data.get("data", {}).get("result")

        if result == "undeliverable":
            raise ValidationError(self.message)

        if result == "risky" and status in ["invalid", "disposable", "unknown"]:
            raise ValidationError(self.message)


class UniqueUsername(object):
    """Checks that there's not another account register with a particular username."""

    def __init__(self, message: str | None = None):
        if not message:
            message = "This username is taken"
        self.message = message

    def __call__(self, form, field):
        user = db.session.scalars(
            select(User).where(User.username == field.data)
        ).one_or_none()

        if user:
            raise ValidationError(self.message)


class UniqueEmail(object):
    """Checks that there's not another account register with a particular email."""

    def __init__(self, message: str | None = None):
        if not message:
            message = "An account already use this email"
        self.message = message

    def __call__(self, form, field):
        user = db.session.scalars(
            select(User).where(User.email == field.data)
        ).one_or_none()

        if user:
            raise ValidationError(self.message)


class RegisteredUsername(object):
    """Validates that there is an account already register with a particular username."""

    def __init__(self, message: str | None = None):
        if not message:
            self.message = "The username don't exist"
        self.message = message

    def __call__(self, form, field):
        try:
            user = db.session.scalars(
                select(User).where(User.username == field.data)
            ).one()
        except:
            raise ValidationError(self.message)


class RegisteredEmail(object):
    """Validates that there is an account already register with a particular email."""

    def __init__(self, message: str | None = None):
        if not message:
            self.message = "The email don't exist"
        self.message = message

    def __call__(self, form, field):
        try:
            user = db.session.scalars(
                select(User).where(User.email == field.data)
            ).one()
        except:
            raise ValidationError(self.message)


class PasswordChecker(object):
    """Checks if a password match with the password of a particular user."""

    def __init__(self, message: str | None = None, username_field: str | None = None):
        if not message:
            self.message = "Password incorrect"
        self.message = message
        self.username_field = username_field

    def __call__(self, form, field):
        username = getattr(form, self.username_field).data
        if not username:
            return

        try:
            user = db.session.scalars(
                select(User).where(User.username == username)
            ).one()
        except:
            return

        if not user.verify_password(field.data):
            raise ValidationError(self.message)
