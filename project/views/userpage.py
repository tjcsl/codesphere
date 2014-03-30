from flask import render_template, flash
from ..utils import ghobject
from ..database import db_session
from ..models import Project, User
from flask import current_app

def get_userpage(user):
    iprojectsraw = db_session.query(Project, User).filter(User.username == user).all()
    x = db_session.query(User).filter(User.username == user).first().id
    iprojects = [i[0].name for i in iprojectsraw if i[0].owner == x]
    current_app.logger.debug(iprojectsraw)
    allprojectsraw = ghobject.get('user/repos')
    allprojects = [i['name'] for i in allprojectsraw]
    uprojects = [i for i in allprojects if i not in iprojects]
    return render_template('userpage.html', user=user, irepos=iprojects, urepos=uprojects, len=len)
