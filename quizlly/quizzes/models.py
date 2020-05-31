from quizlly import db
from datetime import datetime


class Quiz(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    description = db.Column(db.String(200))
    questions = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    rating = db.Column(db.Integer, default=0, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.now())


    def __repr__(self):
        return f'Quiz({self.id}, {self.title})'
