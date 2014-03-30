from flask import render_template, request, session
from flask.ext.socketio import SocketIO, emit, join_room, leave_room
import redis
import os
import urlparse
#import redis
import json
import thread
import logging

from .. import app, socketio

#url = urlparse.urlparse(os.environ.get('REDISCLOUD_URL'))
#r = redis.Redis(host=url.hostname, port=url.port, password=url.password)


@socketio.on('chat', namespace='/sock')
def chat_message(message):
    m = {'user':session['user_name'], 'message': message['message']}
    emit('chat', m, broadcast=True)


#def chat_stream(req):
#    print(req)
#    with req:
#        print(request)
#        ps = r.pubsub()
#        ps.subscribe('chat')
#        for m in ps.listen():
#            print m
#            emit('chat', m)


def chat(user, project):
#    print(request.args.items())
#    thread.start_new_thread(chat_stream, (request,))
    return render_template('chat/chat.html')
