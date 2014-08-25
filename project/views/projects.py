from ..utils.auth import login_required
from ..database import db_session
from ..models import Project, User
from flask import redirect, flash, render_template, url_for, session
from flask.ext.github import GitHubError
from ..utils import privs, ghobject

@login_required
def list_projects(user):
    projects = db_session.query(Project).join(User).filter(User.username == user)
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
    return str(privs.get_user_priv(user, project))

def display_project(user, project):
    uidraw = db_session.query(User).filter(User.username == user).first()
    if uidraw is None:
        flash('Nonexistent user!', 'danger')
        return redirect('/')
    uid = uidraw.id
    project_fromdb = db_session.query(Project).filter(Project.owner == uid, Project.name == project).first()
    if project_fromdb is None:
        flash('Nonexistent project!', 'danger')
        return redirect('/')
    try:
        repoinfo = ghobject.get('repos/%s/%s' % (user, project))
    except GitHubError:
        flash('Couldn\'t fetch from GitHub - is the project private, or has it been deleted?', 'danger')
        return redirect('/u/%s/' % (user))
    branchinfo = ghobject.get('repos/%s/%s/branches/%s' % (user, project, repoinfo['default_branch']))
    commitlist = []
    if 'commit' in branchinfo:
        commitlist.append((branchinfo['commit']['sha'], branchinfo['commit']['commit']['author']['name'], branchinfo['commit']['commit']['author']['date'], branchinfo['commit']['commit']['message']))
    for i in range(4):
        oldcommit = ghobject.get('repos/%s/%s/git/commits/%s' % (user, project, commitlist[i][0]))
        if 'parents' in oldcommit and len(oldcommit['parents']) > 0:
            newcommit = ghobject.get('repos/%s/%s/git/commits/%s' % (user, project, oldcommit['parents'][0]['sha']))
            commitlist.append((newcommit['sha'], newcommit['author']['name'], newcommit['author']['date'], newcommit['message']))
        else:
            break
    return render_template('projects/project.html', commits=commitlist, reponame=project)
