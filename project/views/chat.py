from flask import render_template, request, session
from flask.ext.socketio import SocketIO, emit, send, join_room, leave_room
import redis
import os
import urlparse
import json
import thread
import logging
import re
import base64
from cgi import escape
from sqlalchemy import desc

from .. import app, socketio
from ..utils.auth import login_required
from ..database import db_session
from ..models import Message
from ..utils import ghobject

url = urlparse.urlparse(os.environ.get('REDISCLOUD_URL'))
r = redis.Redis(host=url.hostname, port=url.port, password=url.password)


@socketio.on('chat', namespace='/sock')
def chat_message(message):
    thing = session['username'] if 'username' in session else 'none'
    r.publish(message['room'], thing + ':' + message['message'])
    r.publish("allmsgs", thing + ':' + message['message'])
    m = {'user':session['username'], 'message': escape(message['message'])}
    emit('chat', m, room=message['room'])
    process_code(escape(message['message']),message['room'])
    message = Message(nick=session['username'],content=escape(message['message']),room=message['room'])
    db_session.add(message)
    db_session.commit()

def process_code(m,room, sendto=True):
    file_regex = re.compile(r'(?:of|in) +([\w\d/]*\.[\w\d/]+)')
    messages = db_session.query(Message).order_by(desc(Message.id)).limit(30).all()
    messages = [message.content for message in messages]
    f = None
    for mess in messages[::-1]:
        match = file_regex.findall(mess)
        if match:
            f = match[0]
    match = file_regex.findall(m)
    if match:
        f = match[0]
    if not f:
        return  # Don't continue if a file is not found
    line = None
    line_regex = re.compile(r'(?:lines? +|#)(\d+(?:-\d+)?)')
    match = line_regex.findall(m)
    if match:
        line = match[0]
    if not line:
        return
    owner = room.split('/')[0]
    repo = room.split('/')[1]
    tree = ghobject.get("repos/%s/%s/git/trees/master" % (owner, repo), params={'recursive':'1'})
    fullpath = None
    for i in tree['tree']:
        if i['path'].split('/')[-1] == f.split('/')[-1]:
            fullpath = i['path']
            break
    if not fullpath:
        return
    contents = ghobject.get("repos/%s/%s/contents/%s" % (owner, repo, fullpath))
    if contents['type'] != 'file':
        return
    text = base64.b64decode(contents['content'])
    lines = text.split('\n')
    if '-' in line:
        small = int(line.split('-')[0])-1
        big = int(line.split('-')[1])
        if big > len(lines)-1:
            big = len(lines)-1
        linerange = range(small,big)
    else:
        if int(line) > len(lines):
            emit('code', {'number': 'Error', 'code': 'Line not found'})
            return
        linerange = [int(line)-1]
    mag = len(str(max(linerange)))
    for l in linerange:
        if sendto:
            emit('code',{'number':(' '*(mag-len(str(l+1))))+str(l+1),'code':lines[l]},room=room)
        else:
            emit('code',{'number':(' '*(mag-len(str(l+1))))+str(l+1),'code':lines[l]})




@socketio.on('join', namespace='/sock')
def on_join(data):
    username = session['username']
    room = data['room']
    join_room(room)
    messages = db_session.query(Message).order_by(desc(Message.id)).filter(Message.room == data['room']).limit(10).all()
    emit('join', {'user':username}, broadcast=True)
    emit('backlog','start')
    for m in messages[::-1]:
        mess = {'user':m.nick, 'message': m.content}
        emit('chat', mess)
        process_code(escape(m.content), data['room'], sendto=False)
    emit('backlog','end')



@login_required
def chat(user, project):
    return render_template('chat/chat.html')
