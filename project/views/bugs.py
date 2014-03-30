from flask import render_template, request, session
from ..models import Bug, Project, User
from ..database import db_session
from project.utils.auth import login_required

def browse(user, project):
    bugs = db_session.query(Bug).join(Project).join(User).filter(User.username == user, Project.name == project)
    return render_template("bugs/browse.html", bugs=bugs)

@login_required
def new(user, project):
    if request.method == 'GET':
        return render_template("bugs/new.html", user=user, project=project)
    else:
        return submit(user,project)

def submit(user, project):
    project_id = db_session.query(Project).join(User).filter(User.username == user, Project.name == project).first().id
    submitter = db_session.query(User).filter(User.username == session['username']).first()
    boogs = db_session.query(Bug).filter(Bug.project == project_id).order_by(Bug.bug_id).first()
    boog_id = 1
    if boogs is not None:
        boog_id = boogs.bug_id + 1
    boog = Bug(project_id, request.form['title'], request.form['description'], request.form['priority'], request.form['type'], boog_id, submitter.id)
    db_session.add(boog)
    db_session.commit()
    return "boog creatd"
