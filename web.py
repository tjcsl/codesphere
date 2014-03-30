import project

app = project.app

import logging
from logging.handlers import RotatingFileHandler
handler = RotatingFileHandler("bar.log", maxBytes=1000000)
handler.setLevel(logging.DEBUG)
app.logger.addHandler(handler)
if __name__ == '__main__':
    app.run(port=5000, debug=True)
