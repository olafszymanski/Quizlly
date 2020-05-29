from flask import Flask
from .config import DebugConfig


def create_app(config_class=DebugConfig):
    app = Flask('quizlly')
    app.config.from_object(config_class)

    from .main.views import main

    app.register_blueprint(main)

    return app
