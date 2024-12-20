from flask_wtf import FlaskForm
from wtforms import PasswordField
from wtforms.validators import DataRequired, Length, EqualTo


class ResetPasswordForm(FlaskForm):
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
