from project import app
from project.utils import auth
from flask.ext.github import GitHub
from flask import g, session
from project.models import User
from project.database import db_session

app.secret_key = 'wigwiohowh23tj2pij'

ghobject = GitHub(app)

@ghobject.access_token_getter
def tokenget():
    if 'accesstoken' in session:
        return session['accesstoken']
    return None

def create_organization(orgname):
    org = User.query.filter(User.username == orgname).first()
    if org is None:
        udata = ghobject.get('orgs/%s' % (orgname))
        org = User(email=udata.get('email',None), username=udata['login'], github_access_token=None)
        db_session.add(org)

def create_user(oauth_token):
    udata = ghobject.get('user', params={'access_token': oauth_token})
    user = User.query.filter(User.username == udata['login']).first()
    if user is None:
        user = User(email=udata.get('email',None), username=udata['login'],
                    github_access_token=None)
        db_session.add(user)
        db_session.commit()
    return user
