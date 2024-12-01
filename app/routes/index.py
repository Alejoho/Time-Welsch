from flask import Blueprint, render_template, current_app, request
from app.forms import LoginForm

import requests
import certifi
import ssl

bp = Blueprint("index_routes", __name__)


def verify_recaptcha(recaptcha_response):
    url = "https://www.google.com/recaptcha/api/siteverify"
    data = {
        "secret": current_app.config["RECAPTCHA_PRIVATE_KEY"],
        "response": recaptcha_response,
    }
    context = ssl.create_default_context(cafile=certifi.where())
    response = requests.post(url, data=data, verify=context.verify_mode)
    result = response.json()
    return result.get("success", False)


@bp.route("/", methods=["GET", "POST"])
def index():
    form = LoginForm()
    username = None

    if form.validate_on_submit():
        username = form.username.data
        form.username.data = ""
        recaptcha_response = request.form.get("g-recaptcha-response")
        if verify_recaptcha(recaptcha_response):
            username = "Form submitted successfully!", "success"
        else:
            username = "reCAPTCHA verification failed. Please try again.", "danger"

    return render_template("index.html", form=form, username=username)
