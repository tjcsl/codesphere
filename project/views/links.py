from project.models import ShortenedURL
from flask import redirect

def resolve(id):
    resolved = ShortenedURL.query.filter(ShortenedURL.short == id).one()
    return redirect(resolved.longer)
