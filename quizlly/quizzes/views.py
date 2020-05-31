from quizlly import db
from quizlly.utils import remove_whitespaces
from flask import Blueprint, render_template, session, redirect, url_for, flash
from flask_login import login_required, current_user
from .forms import CreateQuizForm, AddQuestionForm
from .models import Quiz
from .decorators import has_created_quiz, has_created_questions


quizzes = Blueprint('quizzes', __name__)


@quizzes.route('/')
def home():
    return render_template('quizzes/home.html', quizzes=Quiz.query.all())


@quizzes.route('/quiz/create', methods=['GET', 'POST'])
@login_required
def create():
    if session.get('title') and session.get('description') and session.get('question_id'):
        session.pop('title')
        session.pop('description')
        session.pop('question_id')

    form = CreateQuizForm()

    if form.validate_on_submit():
        session['title'] = form.title.data
        session['description'] = form.description.data
        session['question_id'] = 0

        return redirect(url_for('quizzes.question'))

    return render_template('quizzes/create.html', title='Create Quiz', form=form)


@quizzes.route('/quiz/create/question/add', methods=['GET', 'POST'])
@login_required
@has_created_quiz('quizzes.home')
def question():
    form = AddQuestionForm()

    if form.validate_on_submit():
        questions = {
            'question': remove_whitespaces(form.question.data),
            'correct_option': 'option_' + form.correct_option.data,
            'option_1': remove_whitespaces(form.option_1.data),
            'option_2': remove_whitespaces(form.option_2.data),
        }

        if option_3 := remove_whitespaces(form.option_3.data):
            questions['option_3'] = option_3

        session[f'question_{session.get("question_id")}'] = questions

        session['question_id'] = session.get('question_id') + 1

        form.question.data = ''
        form.option_1.data = ''
        form.option_2.data = ''
        form.option_3.data = ''

    return render_template('quizzes/question.html', title=f'Question #{session.get("question_id") + 1}', form=form)


@quizzes.route('/quiz/save')
@login_required
@has_created_quiz('quizzes.home')
@has_created_questions('quizzes.home')
def save():
    title = session.pop('title')
    description = session.pop('description')

    questions = '{'
    for i in range(0, session.pop('question_id')):
        questions += str(session.pop(f'question_{i}')) + ','

    questions += '}'

    quiz = Quiz(title=title, description=description, questions=questions, user=current_user)

    db.session.add(quiz)
    db.session.commit()

    flash('Your quiz has been successfully created!', 'success')

    return redirect(url_for('quizzes.home'))
