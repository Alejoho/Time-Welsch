from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, PasswordField
from wtforms.validators import DataRequired, EqualTo, Email, ValidationError
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


# TODO: Add a validation for the username that should be unique
# TODO: Add a validation for the email that should be unique
class RegisterFrom(FlaskForm):
    username = StringField("Username", validators=[DataRequired("Campo requerido")])
    email = EmailField(
        "Email",
        validators=[
            DataRequired("Campo requerido"),
            Email("Formato de correo inválido"),
            EmailExistence("El correo introducido no existe"),
        ],
    )
    password = PasswordField(
        "Password",
        validators=[
            DataRequired("Campo requerido"),
            EqualTo("confirmation", "Las contraseñas deben coincidir"),
        ],
    )
    confirmation = PasswordField(
        "Confirmation", validators=[DataRequired("Campo requerido")]
    )
