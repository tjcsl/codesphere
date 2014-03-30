from flask import render_template, request, flash, redirect, url_for
from ..models import WhiteboardNotes, Project, User
from ..database import db_session
import json

def view_notes(user, project):
    the_zeroth_thing = db_session.query(User).filter(User.username == user).first().id
    the_first_thing = db_session.query(Project).filter(Project.owner == the_zeroth_thing, Project.name == project).first().id
    the_second_thing = db_session.query(WhiteboardNotes).filter(WhiteboardNotes.project == the_first_thing).first()
    if the_second_thing is not None:
        the_third_thing = the_second_thing
    else:
        the_third_thing = WhiteboardNotes(the_first_thing)
        db_session.add(the_third_thing)
    return render_template("notes/view.html", thing=the_third_thing, user=user, project=project)

def edit_notes(user, project):
    the_other = db_session.query(User).filter(User.username == user).first().id
    that_thing = db_session.query(Project).filter(Project.owner == the_other, Project.name == project).first().id
    potato = db_session.query(WhiteboardNotes).filter(WhiteboardNotes.project == that_thing).first()
    potato.data = request.form["data"]
    potato.tasks = request.form["tasks"]
    db_session.commit()
    flash("Notes updated", "success")
    return redirect(url_for("view_notes", user=user, project=project))
