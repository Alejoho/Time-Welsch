from flask import Flask, render_template, request, flash
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from flask_wtf.recaptcha import RecaptchaField
from wtforms.validators import DataRequired
import requests
import certifi
import ssl

app = Flask(__name__)
app.config["SECRET_KEY"] = "your_secret_key"
app.config["RECAPTCHA_PUBLIC_KEY"] = "your_site_key"
app.config["RECAPTCHA_PRIVATE_KEY"] = "your_secret_key"


class MyForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    recaptcha = RecaptchaField()
    submit = SubmitField("Submit")


def verify_recaptcha(recaptcha_response):
    url = "https://www.google.com/recaptcha/api/siteverify"
    data = {
        "secret": app.config["RECAPTCHA_PRIVATE_KEY"],
        "response": recaptcha_response,
    }
    context = ssl.create_default_context(cafile=certifi.where())
    response = requests.post(url, data=data, verify=context.verify_mode)
    result = response.json()
    return result.get("success", False)


@app.route("/", methods=["GET", "POST"])
def index():
    form = MyForm()
    if form.validate_on_submit():
        recaptcha_response = request.form.get("g-recaptcha-response")
        if verify_recaptcha(recaptcha_response):
            flash("Form submitted successfully!", "success")
        else:
            flash("reCAPTCHA verification failed. Please try again.", "danger")
    return render_template("index.html", form=form)


if __name__ == "__main__":
    app.run(debug=True)
