from flask import current_app
import requests
from app import db
from sqlalchemy import select
from app.models import User
from wtforms.validators import ValidationError


class EmailExistence(object):
    def __init__(self, message=None):
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
            raise ValidationError("Something went wrong")

        if response.status_code != 200:
            raise ValidationError(
                "Unable to verify email address. Please check your connection or try again later"
            )

        data = response.json()
        if not data.get("data", {}).get("result") == "deliverable":
            raise ValidationError(self.message)


class UniqueUsername(object):
    def __init__(self, message=None):
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
    def __init__(self, message=None):
        if not message:
            message = "An account already use this email"
        self.message = message

    def __call__(self, form, field):
        user = db.session.scalars(
            select(User).where(User.email == field.data)
        ).one_or_none()

        if user:
            raise ValidationError(self.message)


class UserExistance(object):
    def __init__(self, message=None):
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


class PasswordChecker(object):
    def __init__(self, message=None, username_field=None):
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
