from flask_wtf import FlaskForm
from wtforms import BooleanField, PasswordField, StringField
from wtforms.validators import DataRequired

from .custom_validators import PasswordChecker, RegisteredUsername


class LoginForm(FlaskForm):
    username = StringField(
        "Usuario",
        validators=[
            DataRequired("Campo requerido"),
            # FIXME: The message is to large and don't show completely
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
