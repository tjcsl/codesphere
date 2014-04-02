from flask import render_template, request, flash, redirect, url_for
from ..models import WhiteboardNotes, Project, User
from ..database import db_session
import json

def view_notes(user, project):
    curruser = db_session.query(User).filter(User.username == user).first().id
    currproject = db_session.query(Project).filter(Project.owner == curruser, Project.name == project).first().id
    storedwhiteboard = db_session.query(WhiteboardNotes).filter(WhiteboardNotes.project == currproject).first()
    if storedwhiteboard is not None:
        newwhiteboard = storedwhiteboard
    else:
        newwhiteboard = WhiteboardNotes(currproject)
        db_session.add(newwhiteboard)
        db_session.commit()
    return render_template("notes/view.html", prid=currproject, notes=json.loads(newwhiteboard.tasks), wbcontents=newwhiteboard, user=user, project=project)

def add_task(pid):
    currwhiteboard = db_session.query(WhiteboardNotes).filter(WhiteboardNotes.project == pid).first()
    storedtasks = json.loads(currwhiteboard.tasks)
    storedtasks.append(request.form["task"])
    currwhiteboard.tasks = json.dumps(storedtasks)
    db_session.commit()
    proj = db_session.query(Project).filter(Project.id == pid).first()
    owner = db_session.query(User).filter(User.id == proj.owner).first()
    return redirect(url_for('view_notes', user=owner.username, project=proj.name))

def del_task(pid):
    currwhiteboard = db_session.query(WhiteboardNotes).filter(WhiteboardNotes.project == pid).first()
    storedtasks = json.loads(currwhiteboard.tasks)
    storedtasks = [i for i in storedtasks if i != request.form["task"]]
    currwhiteboard.tasks = json.dumps(storedtasks)
    db_session.commit()
    proj = db_session.query(Project).filter(Project.id == pid).first()
    owner = db_session.query(User).filter(User.id == proj.owner).first()
    return redirect(url_for('view_notes', user=owner.username, project=proj.name))


def edit_notes(user, project):
    curruser = db_session.query(User).filter(User.username == user).first().id
    proj = db_session.query(Project).filter(Project.owner == curruser, Project.name == project).first().id
    newnotes = db_session.query(WhiteboardNotes).filter(WhiteboardNotes.project == proj).first()
    newnotes.data = request.form["data"]
    db_session.commit()
    flash("Notes updated", "success")
    return redirect(url_for("view_notes", user=user, project=project))
