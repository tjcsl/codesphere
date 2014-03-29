from project import app
from flask.ext.github import GitHub
from flask import g
ghobject = GitHub(app)

@ghobject.access_token_getter
def tokenget():
	user = g.user
	if user is not None:
		return user.github_access_token