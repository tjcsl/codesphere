from ..utils.auth import login_required
from ..database import db_session
from ..models import Project, User
from flask import redirect, flash, render_template, url_for, session
<<<<<<< HEAD
=======
from project.utils import privs
>>>>>>> Implement privaleges

@login_required
def list_projects(user):
    projects = db_session.query(Project, User).filter(User.username == user)
    return redirect(url_for("get_userpage", user=user))
    return "WHAT ARE YOU DOING HERE GO AWAY! --fwilson, 2014"
    return render_template("projects/list.html", projects=projects)

@login_required
def import_project(user, project):
    db_session.add(Project(owner=db_session.query(User).filter(User.username == user)[0].id, name=project))
    db_session.commit()
    if user != session["username"]:
        flash("um wat", "danger")
        return redirect(url_for("get_userpage", user=session["username"]))
    flash("Project added.", "success")
    return redirect(url_for("get_userpage", user=user))

@login_required
def privtest(user, project):
    return str(privs.get_user_priv(user, project, session['username']))
