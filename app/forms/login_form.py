from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, EmailField
from wtforms.validators import DataRequired, Length, Email


class LoginForm(FlaskForm):
    username = StringField(
        "Username",
        validators=[
            DataRequired("Need to enter the email"),
            Length(5, 20, "Need to be between 5 and 20"),
        ],
    )
    email = EmailField(
        "Email",
        validators=[
            DataRequired("Need to enter the email"),
            Email("Invalid email format"),
        ],
    )
    submit = SubmitField("Submit")
