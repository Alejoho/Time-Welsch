from .custom_validators import UniqueUsername, UniqueEmail, EmailExistence
from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, PasswordField
from wtforms.validators import DataRequired, EqualTo, Email, Length


class RegisterFrom(FlaskForm):
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
            EqualTo("confirmation", "Las contraseñas deben coincidir"),
        ],
    )
    confirmation = PasswordField(
        "Repite Contraseña", validators=[DataRequired("Campo requerido")]
    )
