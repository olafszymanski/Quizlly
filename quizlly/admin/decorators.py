from flask import redirect, url_for, flash
from flask_login import current_user
from functools import wraps
from quizlly.users.models import User


def is_admin(redirect_url):
    def is_admin_wrapper(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if User.query.get(current_user.id).admin:
                return func(*args, **kwargs)
            else:
                return redirect(url_for(redirect_url))

        return wrapper

    return is_admin_wrapper
