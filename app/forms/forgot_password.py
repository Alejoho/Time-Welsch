from flask_wtf import FlaskForm
from wtforms import EmailField
from wtforms.validators import DataRequired
from .custom_validators import UniqueEmail, EmailExistence


class ForgotPassword(FlaskForm):
    email = EmailField(
        "Correo",
        validators=[
            DataRequired("Campo requerido"),
            UniqueEmail("No hay cuenta registrada con este correo"),
            EmailExistence("Parece que este correo no está disponible"),
        ],
    )
