from flask import Blueprint, render_template, current_app, url_for
from app.forms import LoginForm
import smtplib
import os

bp = Blueprint("index_routes", __name__)


@bp.route("/", methods=["GET", "POST"])
def index():
    form = LoginForm()
    username = None
    token = None

    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        form.username.data = ""
        form.email.data = ""

        serializer = current_app.config["SERIALIZER"]
        token = serializer.dumps(email, "email_confirmation")
        link = f"127.0.0.1:5000{url_for("index_routes.confirm_email", token=token)}"

        message = f"{username} please follow this link to activate your account: {link}"

        print(message)

        # email_server = smtplib.SMTP("smtp.gmail.com", 587)
        with smtplib.SMTP("smtp.gmail.com", 587) as email_server:
            print("server ready")
            email_server.starttls()
            print("server started")
            email_server.login(os.getenv("GMAIL_ACCOUNT"), os.getenv("GMAIL_PASSWORD"))
            print("server logged")
            email_server.sendmail(os.getenv("GMAIL_ACCOUNT"), email, message)
            print("email sent")

    return render_template("index.html", form=form, username=username, token=token)


@bp.get("/confirm_email/<token>")
def confirm_email(token):
    serializer = current_app.config["SERIALIZER"]

    try:
        email = serializer.loads(token, salt="email_confirmation", max_age=60)
    except:
        return "Something went wrong with the confirmation try again"

    return "The email works"
