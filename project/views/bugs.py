from flask import render_template
from ..models import Bug, Project, User
from ..database import db_session

def browse(user, project):
    bugs = db_session.query(Bug,Project,User).filter(User.username == user, Project.name == project)
    return render_template("bugs/browse.html", bugs=bugs)
