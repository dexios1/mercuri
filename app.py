from flask import render_template
from mercuri import create_app
from flask_migrate import Migrate
from flask_login import login_required
from mercuri.errors import init_error_handlers

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
