# app/forms/login.py

from flask_wtf import FlaskForm
from wtforms import BooleanField, PasswordField, StringField
from wtforms.validators import DataRequired

from .custom_validators import PasswordChecker, RegisteredUsername


class LoginForm(FlaskForm):
    """Form to login a user"""

    username = StringField(
        "Usuario",
        validators=[
            DataRequired("Campo requerido"),
            RegisteredUsername("No hay una cuenta registrada con este usuario"),
        ],
    )

    password = PasswordField(
        "Contraseña",
        validators=[
            DataRequired("Campo requerido"),
            PasswordChecker("Contraseña incorrecta", "username"),
        ],
    )

    remember_me = BooleanField("Recuérdame", default=False)
