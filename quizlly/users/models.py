from quizlly import db, login_manager
from flask_login import UserMixin
from datetime import datetime


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(300))
    quizzes = db.relationship('Quiz', backref='user', lazy=True)
    created_at = db.Column(db.DateTime, default=datetime.now())


    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password


    def __repr__(self):
        return f'User({self.id}, {self.username})'
