from flask import render_template, current_app


def init_error_handlers(app, db):
    @app.errorhandler(404)
    def not_found_error(error):
        return '404', 404

    @app.errorhandler(500)
    def internal_error(error):
        # current_app.logger.error("test string")
        db.session.rollback()
        return '505', 500
