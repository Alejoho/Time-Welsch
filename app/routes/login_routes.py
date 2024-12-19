# LATER: Look up how to organize my imports

from urllib.parse import urlparse
from flask import (
    Blueprint,
    abort,
    current_app,
    flash,
    redirect,
    render_template,
    request,
    url_for,
)
from flask_login import login_user, logout_user
from sqlalchemy import select
from app.forms import LoginForm, ForgotPassword
from app.models import CurrentChapter
from app.models.user import User
from .complements import redirect_authenticated_users, verify_recaptcha
from app import db


bp = Blueprint("login_routes", __name__)


@bp.route("/iniciar_sesion", methods=["GET", "POST"])
@redirect_authenticated_users
def login():
    form = LoginForm()

    if form.validate_on_submit():
        recaptcha_response = request.form.get("g-recaptcha-response")

        if not verify_recaptcha(recaptcha_response):
            flash("reCaptcha fallido. Inténtalo de nuevo", "danger")
            return abort(401)

        user = db.session.scalars(
            select(User).where(User.username == form.username.data)
        ).first()

        # LATER: How to implement the keep me logged in
        login_user(user)

        next_page = request.args.get("next")
        if not next_page or urlparse(next_page).netloc != "":
            next_page = url_for("main_routes.my_route")
        return redirect(next_page)

    return render_template(
        "register_login/login.html",
        form=form,
        site_key=current_app.config["RECAPTCHA_PUBLIC_KEY"],
    )


@bp.get("/cerrar_sesion")
def logout():
    logout_user()
    return redirect(url_for("login_routes.login"))


@bp.post("/demo_confirm")
def demo_confirm():
    user = db.session.scalars(select(User).where(User.username == "demo_confirm")).one()
    login_user(user)
    return redirect(url_for("main_routes.my_route"))


@bp.post("/demo_unconfirm")
def demo_unconfirm():
    user = db.session.scalars(
        select(User).where(User.username == "demo_unconfirm")
    ).one()
    login_user(user)
    return redirect(url_for("main_routes.my_route"))


@bp.post("/demo_delete")
def demo_delete():
    user = User(
        username="demo_delete",
        email="demo@delete.com",
        password="12345678",
        confirmation=True,
    )

    db.session.add(user)
    db.session.commit()

    current_chapter = CurrentChapter(user_id=user.id)

    db.session.add(current_chapter)
    db.session.commit()

    login_user(user)
    return redirect(url_for("main_routes.my_route"))


# NEXT: Design the forgot password logic


@bp.route("/contrasena-olvidada", methods=["GET", "POST"])
def forgot_password():
    form = ForgotPassword()

    return render_template("register_login/forgot_password.html", form=form)


# TODO: Implement the logic to create a demo user with 3 different status.
# 1-Just registerd,
# 2-Half complete the app
# 3-Complete the app
