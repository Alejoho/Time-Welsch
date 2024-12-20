from flask_wtf import FlaskForm
from wtforms import PasswordField
from wtforms.validators import DataRequired, Length, EqualTo


# LATER: Change the name to ResetPasswordForm
# LATER: Move the equal to validation to the second password
class ResetPassword(FlaskForm):
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
