from flask import render_template, current_app

from flask import Blueprint

bp = Blueprint('errors', __name__)


@bp.app_errorhandler(404)
def not_found_error(error):
    return '404', 404


@bp.app_errorhandler(500)
def internal_error(error):
    # current_app.logger.error("test string")
    db.session.rollback()
    return '505', 500
