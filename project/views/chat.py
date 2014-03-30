from flask import render_template, request, session
from flask.ext.socketio import SocketIO, emit, send, join_room, leave_room
import redis
import os
import urlparse
#import redis
import json
import thread
import logging
from cgi import escape

from .. import app, socketio
from ..utils.auth import login_required

#url = urlparse.urlparse(os.environ.get('REDISCLOUD_URL'))
#r = redis.Redis(host=url.hostname, port=url.port, password=url.password)


@socketio.on('chat', namespace='/sock')
def chat_message(message):
    m = {'user':(session['username'] if 'username' in session else '<i>none</i>'), 'message': escape(message['message'])}
    emit('chat', m, room=message['room'])

@socketio.on('join', namespace='/sock')
def on_join(data):
    username = session['username'] if 'username' in session else '<i>none</i>'
    room = data['room']
    join_room(room)
    emit('join', {'user':username})

@login_required
def chat(user, project):
#    print(request.args.items())
#    thread.start_new_thread(chat_stream, (request,))
    return render_template('chat/chat.html')
