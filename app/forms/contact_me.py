from flask_wtf import FlaskForm
from wtforms import EmailField, StringField, TextAreaField
from wtforms.validators import DataRequired, Email

from .custom_validators import EmailExistence


class ContactMeForm(FlaskForm):
    name = StringField("Nombre", validators=[DataRequired("Campo requerido")])
    email = EmailField(
        "Correo",
        validators=[
            DataRequired("Campo requerido"),
            Email("Formato de correo inválido"),
            EmailExistence("El correo introducido no existe"),
        ],
    )
    message = TextAreaField("Mensaje", validators=[DataRequired("Campo requerido")])
