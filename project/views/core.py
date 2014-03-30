from flask import render_template, flash, session, request, url_for, redirect
from ..utils import ghobject, create_user, create_organization
from ..models import User
from ..database import db_session
from flask.ext import github
#import json

def index():
    return render_template("index.html")

def about():
    return render_template("about.html")

def login():
    return ghobject.authorize(scope='user,repo,notifications')

@ghobject.authorized_handler
def ghcallback(oauth_token):
    next_url = request.args.get('next') or url_for('index')
    if oauth_token is None:
        flash("Authorization failed.")
        return redirect(next_url)

    # user = User.query.filter_by(github_access_token=oauth_token).first()
    # if user is None:
    #     udata = ghobject.get('user', params={'access_token': oauth_token})
    #     user = User(email=udata.get('email',None), username=udata['login'], github_access_token=oauth_token)
    #     db_session.add(user)
    user = create_user(oauth_token)
    user_orgs = ghobject.get('user/orgs', params={'access_token': oauth_token})
    org_names = [i['login'] for i in user_orgs]
    [create_organization(i) for i in org_names]

    user.github_access_token = oauth_token
    session['user_id'] = user.id
    session['accesstoken'] = oauth_token
    db_session.commit()
    return redirect(next_url)

def logout():
    session.pop('user_id', None)
    session.pop('accesstoken', None)
    return redirect('/')

def temp_test():
    return str(ghobject.get('orgs/tjcsl/repos'))
