from flask import Blueprint, render_template, current_app
from app.forms import LoginForm

bp = Blueprint("index_routes", __name__)


@bp.route("/", methods=["GET", "POST"])
def index():
    form = LoginForm()
    username = None
    site_key = current_app.config["RECAPTCHA_PUBLIC_KEY"]

    if form.validate_on_submit():
        username = form.username.data
        form.username.data = ""

    return render_template(
        "index.html", form=form, username=username, site_key=site_key
    )
