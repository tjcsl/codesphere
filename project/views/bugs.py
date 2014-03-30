from flask import render_template, request, session, redirect, url_for, flash
from ..models import Bug, Project, User, BugComment
from ..database import db_session
from ..utils.auth import login_required
from ..utils.privs import get_user_priv

def browse(user, project):
    bugs = db_session.query(Bug).join(Project).join(User).filter(User.username == user, Project.name == project)
    return render_template("bugs/browse.html", bugs=bugs)

@login_required
def new(user, project):
    if request.method == 'GET':
        return render_template("bugs/new.html", user=user, project=project)
    else:
        return submit(user,project)

def view_bug(user, project, id):
    if request.method == 'GET':
        bug = db_session.query(Bug).join(Project).join(User).filter(Project.name == project, User.username == user, Bug.bug_id == id).first()
        if bug is None:
            flash('That bug doesn\'t exists!', 'danger')
            return redirect('/')
        else:
            access_level = get_user_priv(user, project)
            comments = db_session.query(BugComment).join(Bug).filter(Bug.bug_id == bug.bug_id, Bug.project == bug.project).all()
            commentors_raw = db_session.query(User).join(BugComment).filter(Bug.bug_id == bug.bug_id, Bug.project == bug.project).all()
            commentors = {}
            submitter = db_session.query(User).join(Bug).filter(Bug.submitter == User.id).first()
            for user in commentors_raw:
                commentors[user.id] = user.username
            return render_template('bugs/view.html', bug_title=bug.title,
                                   type=bug.bug_type, description=bug.description, submitter=submitter.username,
                                   status=bug.status, priority=bug.priority,
                                   comments=comments, commentors=commentors, can_change_status=access_level != 'JHON_DOE')
    else:
        bug = db_session.query(Bug).join(Project).join(User).filter(Project.name == project, User.username == user, Bug.bug_id == id).first()
        if 'new-status' in request.form and request.form['new-status'] != "":
            bug.status = request.form['new-status']
        if 'comment' in request.form:
            commentor = db_session.query(User).filter(User.username == session['username']).first()
            comment = BugComment(bug.id, request.form['comment'], commentor.id)
            db_session.add(comment)
        db_session.commit()
        return redirect(url_for("view_bug", user=user, project=project, id=id))

def submit(user, project):
    project_id = db_session.query(Project).join(User).filter(User.username == user, Project.name == project).first().id
    submitter = db_session.query(User).filter(User.username == session['username']).first()
    boogs = db_session.query(Bug).filter(Bug.project == project_id).order_by(Bug.bug_id.desc()).first()
    boog_id = 1
    if boogs is not None:
        boog_id = boogs.bug_id + 1
    boog = Bug(project_id, request.form['title'], request.form['description'], request.form['priority'], request.form['type'], boog_id, submitter.id)
    db_session.add(boog)
    db_session.commit()
    return redirect(url_for("view_bug", user=user, project=project, id=boog_id))
