from flask import Blueprint, render_template
from sqlalchemy.exc import NoResultFound

bp = Blueprint("error_routes", __name__)


@bp.app_errorhandler(404)
def page_not_found(error):
    return render_template("errors/404.html"), 404


@bp.app_errorhandler(401)
def page_not_found(error):
    return render_template("errors/401.html"), 401


@bp.app_errorhandler(500)
def page_not_found(error):
    return render_template("errors/500.html"), 500


# example of an error handled instead of an status code
@bp.app_errorhandler(NoResultFound)
def no_result_found(error):
    return "No result was found"
