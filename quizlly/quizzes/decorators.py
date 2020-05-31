from flask import session, redirect, url_for
from functools import wraps


def has_created_quiz(redirect_url):
    def has_created_quiz_wrapper(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if session.get('title') and session.get('description') and not session.get('question_id') is None:
                return func(*args, **kwargs)
            else:
                return redirect(url_for(redirect_url))

        return wrapper

    return has_created_quiz_wrapper


def has_created_questions(redirect_url):
    def has_created_questions_wrapper(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if session.get(f'question_{session.get("question_id") - 1}'):
                return func(*args, **kwargs)
            else:
                return redirect(url_for(redirect_url))

        return wrapper

    return has_created_questions_wrapper
