from flask import render_template
from project.models import Bug
from project.database import db_session

def browse(owner, project):
    bugs = db_session.query(Bug).filter(Bug.project == project).llimit(20).all()
    return render_template("bugs/browse.html", bugs=bugs)
