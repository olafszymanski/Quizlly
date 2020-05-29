from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from .config import DebugConfig


db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()


def create_app(config_class=DebugConfig):
    app = Flask('quizlly')
    app.config.from_object(config_class)

    from .main.views import main
    from .users.views import users

    app.register_blueprint(main)
    app.register_blueprint(users)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    return app
