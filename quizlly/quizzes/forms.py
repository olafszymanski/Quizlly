from quizlly.utils import remove_whitespaces
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length, Optional


class CreateQuizForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(min=5, max=100)])
    description = TextAreaField('Description', validators=[DataRequired(), Length(max=200)])
    submit = SubmitField('Next')


class AddQuestionForm(FlaskForm):
    question = StringField('Question', validators=[DataRequired(), Length(min=3, max=200)])
    option_1 = StringField('Option 1', validators=[DataRequired(), Length(min=2, max=100)])
    option_2 = StringField('Option 2', validators=[DataRequired(), Length(min=2, max=100)])
    option_3 = StringField('Option 3', validators=[Optional(), Length(min=2, max=100)])
    correct_option = SelectField('Correct Option', validators=[DataRequired()], choices=[('1', 'Option 1'), ('2', 'Option 2'), ('3', 'Option 3')])
    submit = SubmitField('Next')


    def validate(self):
        if not FlaskForm.validate(self):
            return False

        if not remove_whitespaces(self.option_3.data) and self.correct_option.data == '3':
            self.correct_option.errors.append('Option 3 cannot be empty while selected while selected as an answer!')
            return False

        return True
