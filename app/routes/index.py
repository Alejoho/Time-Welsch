from flask import Blueprint, render_template
from app.forms import LoginForm

bp = Blueprint("index_routes", __name__)


@bp.route("/", methods=["GET", "POST"])
def index():
    form = LoginForm()
    name = None

    if form.validate_on_submit():
        name = form.name.data
        form.name.data = ""

    for error in form.name.errors:
        print(error)

    return render_template("index.html", form=form, name=name)
