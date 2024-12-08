from flask import Blueprint

bp = Blueprint("error_routes", __name__)


# TODO: Add the others error handlers
@bp.app_errorhandler(404)
def page_not_found(error):
    return "this page was not found", 404
