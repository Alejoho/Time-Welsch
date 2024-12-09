from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired
from .custom_validators import UserExistance, PasswordChecker


class LoginForm(FlaskForm):
    username = StringField(
        "Usuario",
        validators=[
            DataRequired("Campo requerido"),
            UserExistance("No hay una cuenta registrada con este nombre de usuario"),
        ],
    )
    password = PasswordField(
        "Contraseña",
        validators=[
            DataRequired("Campo requerido"),
            PasswordChecker("Contraseña incorrecta", "username"),
        ],
    )
