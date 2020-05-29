from quizlly import bcrypt, db
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, current_user, logout_user
from .forms import SignUpForm, LogInForm
from .models import User


users = Blueprint('users', __name__)


@users.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignUpForm()

    if form.validate_on_submit():
        password = bcrypt.generate_password_hash(form.password.data)

        user = User(form.username.data, form.email.data, password)

        db.session.add(user)
        db.session.commit()

        flash('Your account has been created successfully!', 'success')

        return redirect(url_for('main.home'))

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
                return redirect(next_page) if next_page else redirect(url_for('main.home'))
        elif user := User.query.filter_by(email=form.username_or_email.data).first():
            if validate_and_login(user):
                next_page = request.args.get('next')
                return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else:
            flash('User does not exist! Please try using different credentials.', 'danger')

    return render_template('users/login.html', title='Log In', form=form)


@users.route('/logout')
def logout():
    if current_user.is_authenticated:
        logout_user()

    return redirect(url_for('main.home'))
