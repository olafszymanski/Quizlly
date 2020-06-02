from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length, Email


class EditUserForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=6, max=30)])
    email = StringField('E-mail', validators=[DataRequired(), Length(min=5, max=100), Email()])
    submit = SubmitField('Save')
