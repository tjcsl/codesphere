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
        db_session.commit()
    return render_template("notes/view.html", hueid=the_first_thing, notes=json.loads(the_third_thing.tasks), thing=the_third_thing, user=user, project=project)

def add_task(pid):
    thing = db_session.query(WhiteboardNotes).filter(WhiteboardNotes.project == pid).first()
    x = json.loads(thing.tasks)
    x.append(request.form["task"])
    thing.tasks = json.dumps(x)
    db_session.commit()
    stuff = db_session.query(Project).filter(Project.id == pid).first()
    ownerpls = db_session.query(User).filter(User.id == stuff.owner).first()
    return redirect(url_for('view_notes', user=ownerpls.username, project=stuff.name))

def del_task(pid):
    thing = db_session.query(WhiteboardNotes).filter(WhiteboardNotes.project == pid).first()
    x = json.loads(thing.tasks)
    x = [i for i in x if i != request.form["task"]]
    thing.tasks = json.dumps(x)
    db_session.commit()
    stuff = db_session.query(Project).filter(Project.id == pid).first()
    ownerpls = db_session.query(User).filter(User.id == stuff.owner).first()
    return redirect(url_for('view_notes', user=ownerpls.username, project=stuff.name))


def edit_notes(user, project):
    the_other = db_session.query(User).filter(User.username == user).first().id
    that_thing = db_session.query(Project).filter(Project.owner == the_other, Project.name == project).first().id
    potato = db_session.query(WhiteboardNotes).filter(WhiteboardNotes.project == that_thing).first()
    potato.data = request.form["data"]
    db_session.commit()
    flash("Notes updated", "success")
    return redirect(url_for("view_notes", user=user, project=project))
