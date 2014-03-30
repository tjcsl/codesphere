from functools import wraps
from flask import session, redirect, url_for

def login_required(f):
    @wraps(f)
    def wrapped_f(*args, **kwargs):
        if 'user_id' in session and 'accesstoken' in session:
            return f(*args, **kwargs)
        return redirect(url_for('login'))
    return wrapped_f
