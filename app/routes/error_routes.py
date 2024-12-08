from flask import Blueprint

bp = Blueprint("error_routes", __name__)


# LATER: Improve the page of the error handlers
@bp.app_errorhandler(404)
def page_not_found(error):
    return "Esta página no fue encontrada", 404


@bp.app_errorhandler(401)
def page_not_found(error):
    return "Acceso no autorizado", 401


@bp.app_errorhandler(500)
def page_not_found(error):
    return "Error interno del servidor", 500
