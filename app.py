from mercuri.__init__ import create_app, get_db, get_migrate
from flask_migrate import Migrate


app = create_app()
db = get_db()
# register models and push migration
from mercuri.models.user import User
migrate = Migrate(app, db)


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User}


if __name__ == "__main__":
    app.run(debug=True)
