from flask import render_template, flash, session
from ..utils import ghobject
from ..database import db_session
from ..models import Project, User
from flask import current_app

def get_userpage(user):
    iprojectsraw = db_session.query(Project).join(User).filter(User.username == user).all()
    user = db_session.query(User).filter(User.username == user).first()
    if user is None:
        flash('That user hasn\'t logged into our system','danger')
        return render_template('userpage_error.html')
    iprojects = [i.name for i in iprojectsraw if i.owner == user.id]
    allprojectsraw = ghobject.get('user/repos')
    allprojects = [i['name'] for i in allprojectsraw if i['owner']['login'] == session['username']]
    uprojects = [i for i in allprojects if i not in iprojects]
    return render_template('userpage.html', user=user, irepos=iprojects, urepos=uprojects, len=len, session=session)
