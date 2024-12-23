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
from flask_login import current_user, login_required, login_user
from itsdangerous import BadData, BadSignature, SignatureExpired

from app import db
from app.forms import RegisterForm
from app.models import CurrentChapter, User

from .complements import (
    confirm_token,
    handle_confirmation_error,
    send_confirmation_email,
    verify_recaptcha,
)
from .decorators import block_confirmed_users, redirect_authenticated_users

bp = Blueprint("register_routes", __name__)


@bp.route("/registrarse", methods=["GET", "POST"])
@redirect_authenticated_users
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        # reCaptcha verification
        recaptcha_response = request.form.get("g-recaptcha-response")

        if not verify_recaptcha(recaptcha_response):
            flash("reCaptcha fallido. Inténtalo de nuevo", "danger")
            return abort(401)

        # insertion of the new user to the db
        user = User(
            username=form.username.data,
            email=form.email.data,
            password=form.password.data,
        )

        db.session.add(user)

        try:
            db.session.commit()
        except Exception as err:
            print(err)
            db.session.rollback()
            abort(500)

        # Insertion of the related current_chapter with the new user
        current_chapter = CurrentChapter(user_id=user.id)
        db.session.add(current_chapter)

        try:
            db.session.commit()
        except Exception as err:
            print(err)
            db.session.rollback()
            abort(500)

        # Rest of the steps
        send_confirmation_email(user.email)

        login_user(user)

        return redirect(url_for("register_routes.confirmation"))

    return render_template(
        "account_managment/register.html",
        form=form,
        site_key=current_app.config["RECAPTCHA_PUBLIC_KEY"],
    )


@bp.get("/confirmar_email/<token>")
@block_confirmed_users
def confirm_email(token):
    try:
        email = confirm_token(token, current_app.config["ACCOUNT_CONFIRMATION_MAX_AGE"])
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

    user = User.query.where(User.email == email).one()

    user.confirmation = True
    db.session.commit()
    flash("Has confirmado tu cuenta.", "success")

    if not current_user.is_authenticated:
        login_user(user)

    return redirect(url_for("main_routes.my_route"))


@bp.get("/reenviar_confirmacion")
@login_required
@block_confirmed_users
def resend_confirmation():
    send_confirmation_email(current_user.email)
    flash("Un nuevo link de confirmacion ha sido enviado.", "success")
    return redirect(url_for("register_routes.confirmation"))


@bp.route("/no_confirmado")
@login_required
@block_confirmed_users
def unconfirmed():
    if current_user.confirmation:
        return redirect(url_for("main_routes.my_route"))
    return render_template("account_managment/account_confirmation.html")


@bp.get("/confirmacion")
@login_required
@block_confirmed_users
def confirmation():
    return render_template("account_managment/account_confirmation.html", register=True)
