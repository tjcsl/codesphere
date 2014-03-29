from project.views import (
        bugs, core
)
from project import app
from flask.ext.github import github
github = GitHub(app)