from quizlly import bcrypt, db
from quizlly.utils import remove_whitespaces
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, current_user, logout_user, login_required
from .forms import SignUpForm, LogInForm, EditForm, ChangePasswordForm
from .models import User
from quizlly.quizzes.models import Quiz, Review


users = Blueprint('users', __name__)


@users.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignUpForm()

    if form.validate_on_submit():
        password = bcrypt.generate_password_hash(form.password.data)

        user = User(remove_whitespaces(form.username.data), remove_whitespaces(form.email.data), password)

        db.session.add(user)
        db.session.commit()

        login_user(user)

        flash('Your account has been created successfully!', 'success')

        return redirect(url_for('quizzes.home'))

    return render_template('users/signup.html', title='Sign Up', form=form)


@users.route('/login', methods=['GET', 'POST'])
def login():
    form = LogInForm()

    if form.validate_on_submit():
        def validate_and_login(user_object):
            if bcrypt.check_password_hash(user_object.password, form.password.data):
                login_user(user_object)

                return True
            else:
                return False

        if user := User.query.filter_by(username=form.username_or_email.data).first():
            if validate_and_login(user):
                next_page = request.args.get('next')
                return redirect(next_page) if next_page else redirect(url_for('quizzes.home'))
        elif user := User.query.filter_by(email=form.username_or_email.data).first():
            if validate_and_login(user):
                next_page = request.args.get('next')
                return redirect(next_page) if next_page else redirect(url_for('quizzes.home'))
        else:
            flash('User does not exist! Please try using different credentials.', 'danger')

    return render_template('users/login.html', title='Log In', form=form)


@users.route('/logout')
def logout():
    if current_user.is_authenticated:
        logout_user()

    return redirect(url_for('quizzes.home'))


@users.route('/account')
@login_required
def account():
    quizzes = Quiz.query.filter_by(user=current_user)

    return render_template('users/account.html', title='Account', quizzes=quizzes)


@users.route('/account/delete')
@login_required
def delete():
    quizzes = Quiz.query.filter_by(user=current_user).all()
    reviews = Review.query.filter_by(user=current_user).all()

    db.session.delete(current_user)
    for quiz in quizzes:
        db.session.delete(quiz)
    for review in reviews:
        db.session.delete(review)

    db.session.delete(current_user)
    db.session.commit()

    flash('Your account has been successfully deleted!', 'success')

    return redirect(url_for('quizzes.home'))


@users.route('/account/edit', methods=['GET', 'POST'])
@login_required
def edit():
    form = EditForm()

    if request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email

    if form.validate_on_submit():
        current_user.username = remove_whitespaces(form.username.data)
        current_user.email = remove_whitespaces(form.email.data)

        db.session.commit()

        flash('Your profile has been successfully edited!', 'success')

        return redirect(url_for('users.account'))

    return render_template('users/edit.html', title='Edit Account', form=form)


@users.route('/account/password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm()

    if form.validate_on_submit():
        current_user.password = bcrypt.generate_password_hash(form.password.data)

        db.session.commit()

        flash('Your password has been successfully changed!', 'success')

        return redirect(url_for('users.account'))

    return render_template('users/change_password.html', title='Change Password', form=form)


@users.route('/profile/<int:user_id>')
def profile(user_id):
    if current_user.is_authenticated and current_user.id == user_id:
        return redirect(url_for('users.account'))

    user = User.query.get(user_id)
    if user is None:
        flash('Could not find a user with this id!', 'danger')

        return redirect(url_for('quizzes.home'))

    return render_template('users/profile.html', title='Profile', user=user, quizzes=user.quizzes)
