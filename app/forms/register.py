# app/forms/register.py

from flask_wtf import FlaskForm
from wtforms import EmailField, PasswordField, StringField
from wtforms.validators import DataRequired, Email, EqualTo, Length

from .custom_validators import EmailExistence, UniqueEmail, UniqueUsername


class RegisterForm(FlaskForm):
    """Form to register a user"""

    username = StringField(
        "Usuario",
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
