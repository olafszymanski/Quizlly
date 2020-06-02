from quizlly import db
from quizlly.users.models import User
from quizlly.quizzes.models import Quiz, Review
from flask import Blueprint, render_template, flash, redirect, url_for, request
from flask_login import login_required
from .decorators import is_admin
from .forms import EditUserForm


admin_blueprint = Blueprint('admin', __name__)


@admin_blueprint.route('/admin')
@login_required
@is_admin('quizzes.home')
def home():
    users = User.query.all()
    quizzes = Quiz.query.all()
    reviews = Review.query.all()

    return render_template('admin/home.html', title='Admin', users=users, quizzes=quizzes, reviews=reviews)


@admin_blueprint.route('/admin/user/<int:user_id>/edit', methods=['GET', 'POST'])
@login_required
@is_admin('quizzes.home')
def edit_user(user_id):
    form = EditUserForm()

    user = User.query.get(user_id)

    if request.method == 'GET':
        form.username.data = user.username
        form.email.data = user.email

    if form.validate_on_submit():
        user.username = form.username.data
        user.email = form.email.data

        db.session.commit()

        flash('User has been successfully edited!', 'success')

        return redirect(url_for('admin.home'))

    return render_template('admin/edit_user.html', title='Edit User', form=form)


@admin_blueprint.route('/admin/user/<int:user_id>/remove')
@login_required
@is_admin('quizzes.home')
def remove_user(user_id):
    user = User.query.get(user_id)
    if user.admin:
        flash('You cannot remove an admin!')

        return redirect(url_for('admin.home'))

    quizzes = Quiz.query.filter_by(user=user).all()
    reviews = Review.query.filter_by(user=user).all()

    db.session.delete(user)
    for quiz in quizzes:
        db.session.delete(quiz)
    for review in reviews:
        db.session.delete(review)
    db.session.commit()

    flash('User has been removed successfully!', 'success')

    return redirect(url_for('admin.home'))


@admin_blueprint.route('/admin/quiz/<int:quiz_id>/remove')
@login_required
@is_admin('quizzes.home')
def remove_quiz(quiz_id):
    quiz = Quiz.query.get(quiz_id)
    reviews = Review.query.filter_by(quiz=quiz).all()

    db.session.delete(quiz)
    for review in reviews:
        db.session.delete(review)
    db.session.commit()

    flash('Quiz has been removed successfully!', 'success')

    return redirect(url_for('admin.home'))


@admin_blueprint.route('/admin/review/<int:review_id>/remove')
@login_required
@is_admin('quizzes.home')
def remove_review(review_id):
    review = Review.query.get(review_id)

    db.session.delete(review)
    db.session.commit()

    flash('Review has been removed successfully!', 'success')

    return redirect(url_for('admin.home'))
