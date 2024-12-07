from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, ValidationError
from app import db
from sqlalchemy import select
from app.models import User
from flask import abort


# CHECK: The UserExistance validation
# CHECK: The PasswordChecker validation


class UserExistance(object):
    def __init__(self, message):
        if not message:
            self.message = "The username don't exist"
        self.message = message

    def __call__(self, form, field):
        try:
            db.session.scalar(select(User).where(User.username == field.data)).one()
        except:
            raise ValidationError(self.message)


class PasswordChecker(object):
    def __init__(self, message, username):
        if not message:
            self.message = "Password incorrect"
        self.message = message
        self.username = username

    def __call__(self, form, field):
        if not self.username:
            return

        try:
            user = db.session.scalar(
                select(User).where(User.username == self.username)
            ).one()
        except:
            abort(400)

        if not user.verify_password(field.data):
            raise ValidationError(self.message)


class LoginForm(FlaskForm):
    username = StringField(
        "Username",
        validators=[
            DataRequired("Campo requerido"),
            UserExistance("No hay una cuenta registrada con este nombre de usuario"),
        ],
    )
    password = PasswordField(
        "Password",
        validators=[
            DataRequired("Campo requerido"),
            PasswordChecker("Contraseña incorrecta", username),
        ],
    )
