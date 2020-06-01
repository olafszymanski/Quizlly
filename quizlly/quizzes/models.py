from quizlly import db
from datetime import datetime


class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    stars = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.id'))


class Quiz(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    description = db.Column(db.String(200))
    questions = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    reviews = db.relationship('Review', backref='quiz', lazy=True)
    created_at = db.Column(db.DateTime, default=datetime.now())


    def __repr__(self):
        return f'Quiz({self.id}, {self.title})'


    @property
    def rating(self):
        stars = 0
        if len(self.reviews) > 0:
            for review in self.reviews:
                stars += review.stars

            stars /= len(self.reviews)

        return stars
