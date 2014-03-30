from functools import wraps
from flask import session, redirect, url_for, flash
from ..models import User
from ..database import db_session

def login_required(f):
<<<<<<< HEAD
    @wraps(f)
    def wrapped_f(*args, **kwargs):
        if 'user_id' in session and 'accesstoken' in session:
            return f(*args, **kwargs)
        flash('Login is required to access this page.','danger')
        return redirect('/')
    return wrapped_f

=======
    @wraps(f)
    def wrapped_f(*args, **kwargs):
        if 'user_id' in session and 'accesstoken' in session:
            return f(*args, **kwargs)
        return redirect(url_for('login'))
    return wrapped_f
>>>>>>> Implement privaleges
