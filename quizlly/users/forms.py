from flask_wtf import FlaskForm
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from .models import User


class SignUpForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=5, max=30)])
    email = StringField('E-mail', validators=[DataRequired(), Length(min=5, max=100), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=5, max=300)])
    repeat_password = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')


    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('This username is already taken!')


    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('This e-mail is already taken!')


class LogInForm(FlaskForm):
    username_or_email = StringField('Username or E-mail', validators=[DataRequired(), Length(min=5, max=100)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=5, max=300)])
    submit = SubmitField('Log In')


class EditForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=5, max=30)])
    email = StringField('E-mail', validators=[DataRequired(), Length(min=5, max=100), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=5, max=300)])
    submit = SubmitField('Save')


    def validate_username(self, field):
        if user := User.query.filter_by(username=field.data).first():
            if current_user.username != user.username:
                raise ValidationError('This username is already taken!')


    def validate_email(self, field):
        if user := User.query.filter_by(email=field.data).first():
            if current_user.email != user.email:
                raise ValidationError('This e-mail is already taken!')


class ChangePasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired(), Length(min=5, max=300)])
    repeat_password = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Save')
