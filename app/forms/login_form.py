from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, EmailField
from wtforms.validators import DataRequired, Length, Email, ValidationError
from flask import current_app
import requests


class EmailExistence(object):
    def __init__(self, message):
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


class LoginForm(FlaskForm):
    username = StringField(
        "Username",
        validators=[
            DataRequired("Need to enter the email"),
            Length(5, 20, "Need to be between 5 and 20"),
        ],
    )
    email = EmailField(
        "Email",
        validators=[
            DataRequired("Need to enter the email"),
            Email("Invalid email format"),
            EmailExistence("This email doesn't exist"),
        ],
    )
