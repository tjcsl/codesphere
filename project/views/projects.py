from ..utils.auth import login_required
from ..database import db_session
from ..models import Project, User
from flask import redirect, flash, render_template, url_for

@login_required
def list_projects(user):
    projects = db_session.query(Project, User).filter(User.username == user)
    return render_template("projects/list.html", projects=projects)

@login_required
def import_project(user, project):
    db_session.add(Project(owner=db_session.query(User).filter(User.username == user)[0].id, name=project))
    db_session.commit()
    flash("Project added.", "success")
    return redirect(url_for("list_projects", user=user))
