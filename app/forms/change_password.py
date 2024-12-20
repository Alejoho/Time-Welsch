from flask_wtf import FlaskForm
from wtforms import PasswordField, HiddenField
from wtforms.validators import DataRequired, Length, EqualTo
from app.forms.custom_validators import PasswordChecker


class ChangePassword(FlaskForm):
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
