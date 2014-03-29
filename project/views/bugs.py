from flask import render_template
from project.models import Bug
from project.database import db_session

def browse(owner, project):
    owner_id = db_session.query(User).filter(User.username == owner).one()
    project_id = db_session.query(Project).filter(Project.
    bugs = db_session.query(Bug).filter(Bug.project == project).llimit(20).all()
    return render_template("bugs/browse.html", bugs=bugs)
