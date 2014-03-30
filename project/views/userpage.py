from flask import render_template
from ..utils import ghobject
from ..database import db_session
from ..models import Project, User

def get_userpage(user):
    iprojectsraw = db_session.query(Project, User).filter(User.username == user).all()
    iprojects = [i[0].name for i in iprojectsraw]
    allprojectsraw = ghobject.get('user/repos')
    allprojects = [i['name'] for i in allprojectsraw]
    uprojects = [i for i in allprojects if i not in iprojects]
    return render_template('userpage.html', user=user, irepos=iprojects, urepos=uprojects, len=len)
