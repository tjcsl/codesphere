from flask import Flask, g
import os
app = Flask("project")
app.config['GITHUB_CLIENT_ID'] = os.environ['GITHUB_CLIENT_ID']
app.config['GITHUB_CLIENT_SECRET'] = os.environ['GITHUB_CLIENT_SECRET']
app.config['GITHUB_CALLBACK_URL'] = os.environ['GITHUB_CALLBACK_URL']

@app.before_request
def br():
	g.user = None
	if 'user_id' in session:
		g.user = User.query.get(session['user_id'])

import logging
logging.basicConfig(logLevel=logging.DEBUG)
import project.routes
