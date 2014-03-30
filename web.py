import project
from os import getenv

app = project.app

import logging
from logging.handlers import RotatingFileHandler
handler = RotatingFileHandler("bar.log", maxBytes=1000000)
handler.setLevel(logging.DEBUG)
app.logger.addHandler(handler)
if __name__ == '__main__':
    app.run(port=int(getenv("PORT", 5000)), debug=True)
