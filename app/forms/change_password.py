from flask_wtf import FlaskForm
from wtforms import PasswordField, HiddenField
from wtforms.validators import DataRequired, Length, EqualTo
from app.forms.custom_validators import PasswordChecker

# LATER: Document the majority of the code posible


class ChangePassword(FlaskForm):
    username = HiddenField("Usuario")

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
            EqualTo("confirmation", "Las contraseñas deben coincidir"),
        ],
    )

    confirmation = PasswordField(
        "Repite Contraseña", validators=[DataRequired("Campo requerido")]
    )
