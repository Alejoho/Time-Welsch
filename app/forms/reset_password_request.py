from flask_wtf import FlaskForm
from wtforms import EmailField
from wtforms.validators import DataRequired, Email

from .custom_validators import EmailExistence, RegisteredEmail


class ResetPasswordRequestForm(FlaskForm):
    email = EmailField(
        "Correo",
        validators=[
            DataRequired("Campo requerido"),
            Email("Formato de correo inválido"),
            RegisteredEmail("No hay cuenta registrada con este correo"),
            EmailExistence("Parece que este correo no está disponible"),
        ],
    )
