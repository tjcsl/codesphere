from functools import wraps

def login_required(f):
    @wraps(f)
    def wrapped_f(*args, **kwargs):
        return f(*args, **kwargs)
    return wrapped_f
