from mercuri import create_app
from flask_migrate import Migrate

app = create_app()
from mercuri.models import db
db.init_app(app)
# register models and push migration
from mercuri.models.user import User
migrate = Migrate(app, db)

# configure login Manager
from mercuri import login
login.init_app(app)
login.login_view = 'login'


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User}


if __name__ == "__main__":
    app.run(debug=True)
