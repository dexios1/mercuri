import os

from flask import Flask, render_template
from mercuri.config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


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

    from mercuri.blueprints import auth
    app.register_blueprint(auth.bp)

    # index page
    @app.route('/')
    @app.route('/index')
    def index():
        return render_template('index.html')

    return app


app = create_app()
db = SQLAlchemy(app)
migrate = Migrate(app, db)
