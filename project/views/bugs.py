from flask import render_template
from project.models import Bug
from project.database import db_session

def browse():
    bugs = db_session.query(Bug).limit(20).all()
    return render_template("bugs/browse.html", bugs=bugs))
