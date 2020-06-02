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

    from .quizzes.views import quizzes
    from .users.views import users
    from .admin.views import admin_blueprint

    app.register_blueprint(quizzes)
    app.register_blueprint(users)
    app.register_blueprint(admin_blueprint)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'users.login'
    login_manager.login_message = 'You have to log in to access this page'
    login_manager.login_message_category = 'info'

    return app
