from quizlly import db
from quizlly.utils import remove_whitespaces
from flask import Blueprint, render_template, session, redirect, url_for, flash, request
from flask_login import login_required, current_user
from .forms import CreateQuizForm, AddQuestionForm, ReviewForm
from .models import Quiz, Review
from .decorators import has_created_quiz, has_created_questions
import json


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
        question = {
            'question': f'{remove_whitespaces(form.question.data)}',
            'correct_option': f'option_{form.correct_option.data}',
            'option_1': f'{remove_whitespaces(form.option_1.data)}',
            'option_2': f'{remove_whitespaces(form.option_2.data)}',
        }

        if option_3 := remove_whitespaces(form.option_3.data):
            question['option_3'] = f'{option_3}'

        session[f'question_{session.get("question_id")}'] = question

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

    questions = []
    for i in range(0, session.pop('question_id')):
        question = str(session.pop(f'question_{i}'))
        question = question.replace("'", '"')

        questions.append(question)

    quiz = Quiz(title=title, description=description, questions=str(questions), user=current_user)

    db.session.add(quiz)
    db.session.commit()

    flash('Your quiz has been successfully created!', 'success')

    return redirect(url_for('quizzes.home'))


@quizzes.route('/quiz/<int:quiz_id>')
@login_required
def quiz(quiz_id):
    if quiz := Quiz.query.get(quiz_id):
        session['quiz_id'] = quiz.id
    else:
        flash('No quiz with this id found!', 'danger')

        return redirect(url_for('quizzes.home'))

    return render_template('/quizzes/quiz.html', title='Quiz', quiz=quiz)


@quizzes.route('/quiz/<int:quiz_id>/question/<int:question_id>', methods=['GET', 'POST'])
@login_required
def quiz_question(quiz_id, question_id):
    if quiz_id != session.get('quiz_id'):
        flash('You are trying to answer question of a test that you have not yet taken!', 'danger')

        return redirect(url_for('quizzes.home'))

    if request.method == 'POST':
        answer = request.form.get("answer")
        session[f'quiz_answer_{question_id - 1}'] = f'option_{answer}'

    if quiz_questions := Quiz.query.get(quiz_id).questions:
        session['quiz_questions'] = quiz_questions
        questions = quiz_questions
        questions = questions.replace("'", '')
        questions = json.loads(questions)
        session['quiz_question_id'] = question_id

        if question_id >= len(questions):
            flash('No question with this id found!', 'danger')

            return redirect(url_for('quizzes.quiz', quiz_id=quiz_id))

        return render_template('quizzes/quiz_question.html', title=f'Question #{question_id}', question=questions[question_id], questions_length=len(questions))
    else:
        flash('No quiz with this id found!', 'danger')

        return redirect(url_for('quizzes.home'))


@quizzes.route('/quiz/<int:quiz_id>/finish', methods=['GET', 'POST'])
@login_required
def quiz_finish(quiz_id):
    if quiz_id != session.get('quiz_id'):
        flash('You are trying to finish a test that you have not yet taken!', 'danger')

        return redirect(url_for('quizzes.home'))

    questions = session.get('quiz_questions')
    questions = questions.replace("'", '')
    questions = json.loads(questions)

    score = 0

    question_id = session.get('quiz_question_id')

    if answer := request.form.get("answer")[-1]:
        session[f'quiz_answer_{question_id}'] = answer
        question_id += 1

    for i in range(0, question_id):
        correct_option = questions[i]['correct_option'][-1]
        answer = session.get(f'quiz_answer_{i}')[-1]
        if answer == correct_option:
            score += 100

    score /= len(questions)

    return render_template('quizzes/quiz_finish.html', title='Finish', quiz=Quiz.query.get(quiz_id), score=int(score))


@quizzes.route('/quiz/<int:quiz_id>/review', methods=['GET', 'POST'])
@login_required
def review(quiz_id):
    quiz = Quiz.query.get(quiz_id)
    if quiz is None:
        flash('Quiz with this id does not exist!', 'danger')

        return redirect(url_for('quizzes.home'))

    form = ReviewForm()

    if form.validate_on_submit():
        review = Review.query.filter_by(user=current_user).filter_by(quiz=quiz).first()
        if review is None:
            review = Review(stars=form.review.data, user=current_user, quiz=quiz)

            db.session.add(review)

            flash('Your review has been successfully added!', 'success')
        else:
            review.stars = form.review.data

            flash('Your review has been successfully updated!', 'success')

        db.session.commit()

        return redirect(url_for('quizzes.home'))

    return render_template('quizzes/review.html', title='Review', quiz=quiz, form=form)
