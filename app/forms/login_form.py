from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import DataRequired, Length


class LoginForm(FlaskForm):
    name = StringField(
        "Name", validators=[Length(5, 10, "Need to be between 5 and 10")]
    )
    age = IntegerField("Age", validators=[DataRequired("Need to enter this")])
    # sex = StringField("Sex")
    submit = SubmitField("Submit")
