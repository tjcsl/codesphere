from flask import render_template, request
from ..models import Bug, Project, User
from ..database import db_session

def browse(user, project):
    bugs = db_session.query(Bug).join(Project).join(User).filter(User.username == user, Project.name == project)
    return render_template("bugs/browse.html", bugs=bugs)

def new(user, project):
    return render_template("bugs/new.html", user=user, project=project)

def submit(user, project):
    request.form
