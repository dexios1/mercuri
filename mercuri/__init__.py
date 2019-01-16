from flask import Flask, current_app, request
from mercuri.config import Config
from flask_login import LoginManager
from flask_babel import Babel
import logging
from logging.handlers import SMTPHandler
from logging.handlers import RotatingFileHandler
import os
import sentry_sdk
from flask_migrate import Migrate
from mercuri.helpers.errors import init_error_handlers
from mercuri.models import db

# register models and push migration
login = LoginManager()
babel = Babel()
# TODO: continue adding babel to the app
migrate = Migrate()


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(Config)

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    app.secret_key = app.config['SECRET_KEY']

    db.init_app(app)
    from mercuri.models.user import User
    migrate.init_app(app, db)
    login.init_app(app)
    login.login_view = 'auth.login'
    # initialize extensions used in app
    babel.init_app(app)
    # configure sentry
    sentry_sdk.init(app.config['SENTRY_URL'])

    from mercuri.blueprints import auth
    app.register_blueprint(auth)

    from mercuri.api import bp as api_bp
    app.register_blueprint(api_bp, url_prefix='/api')

    init_error_handlers(app, db)

    # send error logs to email
    if not app.debug and not app.testing:
        if app.config['MAIL_SERVER']:
            auth = None
            if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
                auth = (app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
            secure = None
            if app.config['MAIL_USE_TLS']:
                secure = ()
            mail_handler = SMTPHandler(
                mailhost=(app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
                fromaddr='no-reply@' + app.config['MAIL_SERVER'],
                toaddrs=app.config['ADMINS'], subject='Mercuri Error Logs',
                credentials=auth, secure=secure)
            mail_handler.setLevel(logging.ERROR)
            app.logger.addHandler(mail_handler)
            if app.config['LOG_TO_STDOUT']:
                stream_handler = logging.StreamHandler()
                stream_handler.setLevel(logging.INFO)
                app.logger.addHandler(stream_handler)
            else:
                # send error logs to file
                if not os.path.exists('logs'):
                    os.mkdir('logs')
                file_handler = RotatingFileHandler('logs/mercuri.log', maxBytes=10240,
                                                   backupCount=10)
                file_handler.setFormatter(logging.Formatter(
                    '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
                file_handler.setLevel(logging.INFO)
                app.logger.addHandler(file_handler)

                app.logger.setLevel(logging.INFO)
                app.logger.info('Mercuri')

    return app


@babel.localeselector
def get_locale():
    return request.accept_languages.best_match(current_app.config['LANGUAGES'])

