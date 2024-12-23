# app/forms/reset_password.py

from flask_wtf import FlaskForm
from wtforms import PasswordField
from wtforms.validators import DataRequired, EqualTo, Length


class ResetPasswordForm(FlaskForm):
    """Form to reset a forgotten password"""

    password = PasswordField(
        "Contraseña",
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
            EqualTo("password", "Las contraseñas deben coincidir"),
        ],
    )
