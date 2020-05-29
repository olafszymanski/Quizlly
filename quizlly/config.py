import os


class Config:
    DEBUG = False
    SECRET_KEY = os.getenv('QUIZLLY_SECRET_KEY')


class DebugConfig(Config):
    DEBUG = True
