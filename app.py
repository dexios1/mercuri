from flask import render_template
from mercuri import create_app
from flask_migrate import Migrate
from flask_login import login_required
# from mercuri.errors import init_error_handlers


app = create_app()


# configure login Manager


# configure Mail
from mercuri.helpers.email import mail
mail.init_app(app)


# init_error_handlers(app, db)


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
    app.run(port=8000)
