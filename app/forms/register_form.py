from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, PasswordField
from wtforms.validators import DataRequired, EqualTo, Email, ValidationError, Length
from flask import current_app
import requests
from app import db
from sqlalchemy import select
from app.models import User


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


class UniqueUsername(object):
    def __init__(self, message):
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
    def __init__(self, message):
        if not message:
            message = "An account already use this email"
        self.message = message

    def __call__(self, form, field):
        user = db.session.scalars(
            select(User).where(User.username == field.data)
        ).one_or_none()

        if user:
            raise ValidationError(self.message)


# CHECK: The UniqueUsername validation
# CHECK: The UniqueEmail validation
class RegisterFrom(FlaskForm):
    username = StringField(
        "Username",
        validators=[
            DataRequired("Campo requerido"),
            Length(5, 50, "El nombre the usuario debe tener entre 5 y 50 caracteres"),
            UniqueUsername("Este nombre de usuario ya esta en uso"),
        ],
    )
    email = EmailField(
        "Email",
        validators=[
            DataRequired("Campo requerido"),
            Email("Formato de correo inválido"),
            UniqueEmail("Una cuenta ya está usando este correo"),
            EmailExistence("El correo introducido no existe"),
        ],
    )
    password = PasswordField(
        "Password",
        validators=[
            DataRequired("Campo requerido"),
            Length(
                min=8,
                message="La contraseña debe tener más de 8 caracteres",
            ),
            EqualTo("confirmation", "Las contraseñas deben coincidir"),
        ],
    )
    confirmation = PasswordField(
        "Confirmation", validators=[DataRequired("Campo requerido")]
    )
