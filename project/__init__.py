from flask import Flask, g, session
from flask.ext.socketio import SocketIO
import os
from project.models import User
app = Flask("project")
socketio = SocketIO(app)
app.config['GITHUB_CLIENT_ID'] = os.environ['GITHUB_CLIENT_ID']
app.config['GITHUB_CLIENT_SECRET'] = os.environ['GITHUB_CLIENT_SECRET']
app.config['GITHUB_CALLBACK_URL'] = os.environ['GITHUB_CALLBACK_URL']
# @app.before_request
# def br():
# 	session['user'] = None
# 	if 'user_id' in session:
# 		session['user'] = User.query.get(session['user_id'])

#import logging
#logging.basicConfig(logLevel=logging.DEBUG)
app.secret_key = "PLS DONT HAX US"
import project.routes
