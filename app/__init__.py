from flask import Flask
from flask_bootstrap import Bootstrap
from .config import Config

#Se importa el blueprint auth
from .auth import auth

def create_app():
    app = Flask(__name__)
    bootstrap = Bootstrap(app)
    app.config.from_object(Config)

    #Se registra el blueprint auth
    app.register_blueprint(auth)
    return app