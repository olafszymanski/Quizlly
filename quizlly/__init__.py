from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .config import DebugConfig


db = SQLAlchemy()


def create_app(config_class=DebugConfig):
    app = Flask('quizlly')
    app.config.from_object(config_class)

    from .main.views import main

    app.register_blueprint(main)

    db.init_app(app)

    return app
