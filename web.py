import project
import logging
from os import getenv

app = project.app
app.debug = True
port = int(getenv("PORT", 5000))
socketio = project.socketio

from logging.handlers import RotatingFileHandler
handler = RotatingFileHandler("bar.log", maxBytes=1000000)
handler.setLevel(logging.DEBUG)
app.logger.addHandler(handler)
if __name__ == '__main__':
    socketio.run(app, port=port, host='0.0.0.0')
