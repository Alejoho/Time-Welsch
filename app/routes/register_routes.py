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
from flask_login import login_user, login_required, current_user

from app.models import CurrentChapter
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
        "register_login/register.html",
        form=form,
        site_key=current_app.config["RECAPTCHA_PUBLIC_KEY"],
    )


@bp.get("/confirmar_email/<token>")
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

    # CHECK: The user is logged in (it has not been confirmed) so the current_user variable is instanciated.
    # I query the db and return a result with the same user and set the confirm field to true.
    # After I the commit the confirm field is updated in the current user as well?

    user = User.query.where(User.email == email).one()

    if user.confirmation:
        flash("Cuenta ya confirmada.", "info")
    else:
        user.confirmation = True
        db.session.commit()
        flash("Has confirmado tu cuenta.", "success")

    if not current_user.is_authenticated:
        login_user(user)

    return redirect(url_for("main_routes.my_route"))


@bp.get("/reenviar_confirmacion")
@login_required
@block_confirmed
def resend_confirmation():
    send_confirmation_email(current_user.email)
    flash("Un nuevo link de confirmacion ha sido enviado.", "success")
    return redirect(url_for("register_routes.confirmation"))


@bp.route("/no_confirmado")
@login_required
@block_confirmed
def unconfirmed():
    if current_user.confirmation:
        return redirect(url_for("main_routes.my_route"))
    return render_template("register_login/confirmation.html")


@bp.get("/confirmacion")
@login_required
@block_confirmed
def confirmation():
    return render_template("register_login/confirmation.html", register=True)
