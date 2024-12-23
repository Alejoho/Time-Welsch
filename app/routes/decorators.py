from functools import wraps

from flask import abort, flash, redirect, url_for
from flask_login import current_user


def redirect_authenticated_users(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if current_user.is_authenticated:
            flash("Tu sesión ya está iniciada", "info")
            return redirect(url_for("main_routes.my_route"))
        return func(*args, **kwargs)

    return decorated_function


def block_confirmed_users(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if current_user.is_authenticated and current_user.confirmation is True:
            return abort(401)
        return func(*args, **kwargs)

    return decorated_function


def block_unconfirmed_users(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if current_user.confirmation is False:
            flash("Por favor confirma tu cuenta!", "warning")
            return redirect(url_for("register_routes.unconfirmed"))
        return func(*args, **kwargs)

    return decorated_function


def check_chapter(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        chapter_number = args[0] if args else kwargs.get("chapter_number")
        if chapter_number > current_user.current_chapter:
            flash("Faltan capítulos por leer.", "info")
            return redirect(url_for("main_routes.my_route"))
        return func(*args, **kwargs)

    return decorated_function
