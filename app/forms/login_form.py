from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import DataRequired
from .custom_validators import RegisteredUsername, PasswordChecker


class LoginForm(FlaskForm):
    username = StringField(
        "Usuario",
        validators=[
            DataRequired("Campo requerido"),
            RegisteredUsername(
                "No hay una cuenta registrada con este nombre de usuario"
            ),
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
