# app/forms/change_password.py

from flask_wtf import FlaskForm
from wtforms import HiddenField, PasswordField
from wtforms.validators import DataRequired, EqualTo, Length

from app.forms.custom_validators import PasswordChecker


class ChangePasswordForm(FlaskForm):
    """Form to change the password of a logged in user."""

    username = HiddenField()

    old_password = PasswordField(
        "Contraseña Antigua",
        validators=[
            DataRequired("Campo requerido"),
            PasswordChecker("Contraseña incorrecta", "username"),
        ],
    )

    new_password = PasswordField(
        "Contraseña Nueva",
        validators=[
            DataRequired("Campo requerido"),
            Length(
                min=8,
                message="La contraseña debe tener más de 8 caracteres",
            ),
        ],
    )

    confirmation = PasswordField(
        "Repite Contraseña",
        validators=[
            DataRequired("Campo requerido"),
            EqualTo("new_password", "Las contraseñas deben coincidir"),
        ],
    )
