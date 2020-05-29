import os


class Config:
    DEBUG = False
    SECRET_KEY = os.getenv('QUIZLLY_SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.getenv('QUIZLLY_DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DebugConfig(Config):
    DEBUG = True
