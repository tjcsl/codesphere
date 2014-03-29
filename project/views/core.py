from flask import render_template, flash, session, request, url_for, redirect
from project.utils import ghobject
from project.models import User
from flask.ext import github
import json

def index():
    return render_template("index.html")

def about():
    return render_template("about.html")

def login():
	if session.get('user_id', None) is None:
		return ghobject.authorize(scope='user,repo,notifications')
	else:
		return redirect('/')

@ghobject.authorized_handler
def ghcallback(oauth_token):
	next_url = request.args.get('next') or url_for('index')
	if oauth_token is None:
		flash("Authorization failed.")
		return redirect(next_url)

	user = User.query.filter_by(github_access_token=oauth_token).first()
	if user is None:
		udata = json.loads(ghobject.get('user'))
		user = User(email=udata['email'], username=udata['login'], github_access_token=github_access_token)
		user.save()

	user.github_access_token = oauth_token
	user.save()
	session['user_id'] = user.username
	return redirect(next_url)

def logout():
	session.pop('user_id', None)
	return redirect('/')

def temp_test():
	return ghobject.get('orgs/tjcsl/repos')