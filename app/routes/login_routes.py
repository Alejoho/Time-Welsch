# app/routes/login_routes.py

from urllib.parse import urlparse

from flask import (
    Blueprint,
    abort,
    current_app,
    flash,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
from flask_login import login_user, logout_user
from itsdangerous import BadData, BadSignature, SignatureExpired
from sqlalchemy import select

from app import db
from app.forms import LoginForm, ResetPasswordForm, ResetPasswordRequestForm
from app.models import User

from .complements import (
    confirm_token,
    create_demo_user,
    handle_reset_password_error,
    send_reset_password_email,
    verify_recaptcha,
)
from .decorators import redirect_authenticated_users

bp = Blueprint("login_routes", __name__)


@bp.route("/iniciar_sesion", methods=["GET", "POST"])
@redirect_authenticated_users
def login():
    form = LoginForm()

    if form.validate_on_submit():
        # Verifies the reCaptcha score
        recaptcha_response = request.form.get("g-recaptcha-response")

        if not verify_recaptcha(recaptcha_response):
            flash("reCaptcha fallido. Inténtalo de nuevo", "danger")
            return abort(401)

        # Login the user
        user = db.session.scalars(
            select(User).where(User.username == form.username.data)
        ).first()

        login_user(user, remember=form.remember_me.data)

        # Redirects the user to a login required page
        next_page = request.args.get("next")
        if not next_page or urlparse(next_page).netloc != "":
            next_page = url_for("main_routes.my_route")
        return redirect(next_page)

    return render_template(
        "account_managment/login.html",
        form=form,
        site_key=current_app.config["RECAPTCHA_PUBLIC_KEY"],
    )


@bp.get("/cerrar_sesion")
def logout():
    logout_user()
    return redirect(url_for("login_routes.login"))


@bp.route("/reestablecer-contrasena", methods=["GET", "POST"])
@redirect_authenticated_users
def reset_password_request():
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        # Verifies the reCaptcha score
        recaptcha_response = request.form.get("g-recaptcha-response")

        if not verify_recaptcha(recaptcha_response):
            flash("reCaptcha fallido. Inténtalo de nuevo", "danger")
            return abort(401)

        send_reset_password_email(form.email.data)
        return render_template("account_managment/reset_password_confirmation.html")

    return render_template("account_managment/reset_password_request.html", form=form)


@bp.route("/reestablecer-contrasena/<token>", methods=["GET", "POST"])
@redirect_authenticated_users
def reset_password(token):
    # Deserialized the token to obtain the email
    try:
        email = confirm_token(token, current_app.config["RESET_PASSWORD_MAX_AGE"])
    except SignatureExpired:
        return handle_reset_password_error(
            "El link de reestablecer contraseña que intentaste ha expirado. Inténtalo de nuevo."
        )
    except BadSignature:
        return handle_reset_password_error(
            "El link de reestablecer contraseña que intentaste es inválido.  Inténtalo de nuevo."
        )
    except BadData:
        return handle_reset_password_error(
            "El link de reestablecer contraseña que intentaste es inválido debido a malos datos. Inténtalo de nuevo."
        )

    form = ResetPasswordForm()

    if form.validate_on_submit():
        # Verifies the reCaptcha score
        recaptcha_response = request.form.get("g-recaptcha-response")

        if not verify_recaptcha(recaptcha_response):
            flash("reCaptcha fallido. Inténtalo de nuevo", "danger")
            return abort(401)

        # Sets the new password
        user = db.session.scalars(select(User).where(User.email == email)).one()
        user.password = form.password.data
        db.session.commit()

        flash("Contraseña reestablecida.", "success")
        return redirect(url_for("login_routes.login"))

    return render_template("account_managment/reset_password.html", form=form)


@bp.get("/iniciar_sesion_usuario_demo/<level>")
def login_user_demo(level):
    if level == "principiante":
        user = create_demo_user(name="demo_principiante")
    elif level == "intermedio":
        user = create_demo_user(16, "demo_intermedio")
    elif level == "avanzado":
        user = create_demo_user(32, "demo_avanzado")
    else:
        abort(400)

    login_user(user)
    session["is_demo"] = True
    session.permanent = False

    return redirect(url_for("main_routes.my_route"))
