import project
from os import getenv

app = project.app
app.debug=True
app.port=5000
app.threaded = True
socketio = project.socketio

import logging
from logging.handlers import RotatingFileHandler
handler = RotatingFileHandler("bar.log", maxBytes=1000000)
handler.setLevel(logging.DEBUG)
app.logger.addHandler(handler)
if __name__ == '__main__':
    socketio.run(app)
