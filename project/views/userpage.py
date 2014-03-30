from flask import render_template
from ..utils import ghobject
from ..database import db_session
from ..models import Project, User

def get_userpage(user):
	asdf = user
	iprojects = db_session.query(Project, User).filter(User.username == asdf).all()
	allprojects = ghobject.get('user/repos')
	print str(allprojects)
	return render_template('userpage.html', irepos=iprojects)
