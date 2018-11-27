from flask import render_template
from mercuri import create_app
from flask_migrate import Migrate
from flask_login import login_required
from mercuri.errors import init_error_handlers
import sentry_sdk

app = create_app()
from mercuri.models import db
db.init_app(app)
# register models and push migration
from mercuri.models.user import User
migrate = Migrate(app, db)

# configure login Manager
from mercuri import login
login.init_app(app)
login.login_view = 'auth.login'


init_error_handlers(app, db)
# configure sentry
sentry_sdk.init("https://bb0a3cdad37040938b082d9a446edfd7@sentry.io/1331904")


# index page
@app.route('/')
@app.route('/index')
@login_required
def index():
    return render_template('index.html')


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User}


if __name__ == "__main__":
    app.run()
