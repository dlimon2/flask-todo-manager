#from mariadb_service import db
from flask import Flask
from flask_bootstrap import Bootstrap
from .config import Config
from flask_login import LoginManager
from .models import User

login_manager = LoginManager()

from .auth import auth
login_manager.login_view = 'auth.login'
@login_manager.user_loader
def load_user(user_id):
    if user_id is not None:
        return User.query.get(user_id)
    return None

def create_app():
    app = Flask(__name__)
    bootstrap = Bootstrap(app)
    app.config.from_object(Config)

    from .extensions import db
    db.init_app(app)

    login_manager.init_app(app)
    app.register_blueprint(auth)

    with app.app_context():
        db.create_all()
    return app