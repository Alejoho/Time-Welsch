from flask import (
    Blueprint,
    render_template,
    current_app,
    request,
    abort,
    redirect,
    url_for,
    flash,
)
from app.forms import RegisterFrom
from app.models import User
from app import db
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select
from flask_login import login_user, login_required, current_user
from .complements import (
    confirm_token,
    send_confirmation_email,
    verify_recaptcha,
    handle_confirmation_error,
    block_confirmed,
    redirect_authenticated_users,
)
from itsdangerous import SignatureExpired, BadSignature, BadData

bp = Blueprint("register_routes", __name__)


@bp.route("/registrarse", methods=["GET", "POST"])
@redirect_authenticated_users
def register():
    form = RegisterFrom()

    if form.validate_on_submit():
        recaptcha_response = request.form.get("g-recaptcha-response")

        if not verify_recaptcha(recaptcha_response):
            flash("reCaptcha fallido. Inténtalo de nuevo", "danger")
            return abort(401)

        user = User(
            username=form.username.data,
            email=form.email.data,
            password=form.password.data,
        )

        db.session.add(user)

        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()

            existing_user = db.session.scalars(
                select(User).where(
                    (User.username == form.username.data)
                    | (User.email == form.email.data)
                )
            ).one_or_none()

            if existing_user.username == form.username.data:
                form.username.errors.append("Este nombre de usuario ya esta en uso")
            if existing_user.email == form.email.data:
                form.email.errors.append("Una cuenta ya está usando este correo")

        send_confirmation_email(user.email)

        login_user(user)

        return redirect(url_for("home_routes.confirmation"))

    return render_template(
        "register.html", form=form, site_key=current_app.config["RECAPTCHA_PUBLIC_KEY"]
    )


@bp.get("/confirmar_email/<token>")
@login_required
@block_confirmed
def confirm_email(token):
    try:
        email = confirm_token(token)
    except SignatureExpired:
        return handle_confirmation_error(
            "El link de confirmación que intentaste ha expirado."
        )
    except BadSignature:
        return handle_confirmation_error(
            "El link de confirmación que intentaste es inválido."
        )
    except BadData:
        return handle_confirmation_error(
            "El link de confirmación que intentaste es inválido debido a malos datos."
        )

    if current_user.confirmation:
        flash("Cuenta ya confirmada.", "success")
    else:
        current_user.confirmation = True
        db.session.commit()
        flash("Has confirmado tu cuenta.", "success")
    return redirect(url_for("main_routes.my_route"))


@bp.get("/reenviar_confirmacion")
@login_required
@block_confirmed
def resend_confirmation():
    send_confirmation_email(current_user.email)
    flash("Un nuevo link de confirmacion ha sido enviado.", "success")
    return redirect(url_for("home_routes.confirmation"))


@bp.route("/no_confirmado")
@login_required
@block_confirmed
def unconfirmed():
    if current_user.confirmation:
        return redirect(url_for("main_routes.my_route"))
    return render_template("confirmation.html")


@bp.get("/confirmacion")
@login_required
@block_confirmed
def confirmation():
    return render_template("confirmation.html", register=True)
