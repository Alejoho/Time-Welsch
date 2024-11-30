from flask import Blueprint, render_template, current_app
from app.forms import LoginForm

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

    return render_template("index.html", form=form, username=username, token=token)


@bp.get("/confirm_email/<token>")
def confirm_email(token):
    serializer = current_app.config["SERIALIZER"]

    try:
        email = serializer.loads(token, salt="email_confirmation", max_age=10)
    except:
        return "Something went wrong with the confirmation try again"

    return "The email works"
