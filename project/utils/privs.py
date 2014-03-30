from flask import session
import json
from project.database import db_session
from project.models import UserPrivilege, User, Project
import project.utils

def get_user_priv(user_name, repo_name, to_get_user):
    priv = db_session.query(UserPrivilege).join(User).join(Project).filter(Project.name == repo_name, User.username == user_name).first()
    if priv is None:
        req_string = 'repos/%s/%s/contributors' % (user_name, repo_name)
        contributors = project.utils.ghobject.get(req_string)
        contributor_unames = [i['login'] for i in contributors]
        project_id = db_session.query(Project).join(User).filter(User.username == user_name).filter(Project.name == repo_name).first().id
        user_id = db_session.query(User).filter(User.username == to_get_user).first().id
        if to_get_user in contributor_unames:
            priv = UserPrivilege(project_id, user_id,'CONTRIBUTER')
        else:
            priv = UserPrivilege(project_id, user_id,'JHON_DOE')
        db_session.add(priv)
        db_session.commit()
    return priv.level
