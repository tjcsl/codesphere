from project import app
from project.utils import auth
from flask.ext.github import GitHub
from flask import g, session

app.secret_key = 'wigwiohowh23tj2pij'

ghobject = GitHub(app)

@ghobject.access_token_getter
def tokenget():
    if 'accesstoken' in session:
        return session['accesstoken']
    return None
