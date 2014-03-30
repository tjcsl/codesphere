from ..models import ShortenedURL
from flask import redirect, request, session, render_template, flash
from ..utils.auth import login_required
from ..database import db_session

def resolve(id):
    resolved = ShortenedURL.query.filter(ShortenedURL.short == id).one()
    return redirect(resolved.longer)

@login_required
def shortener():
    if request.method == 'POST':
        if request.form['short'] == '' or request.form['long'] == '':
            flash("Both fields are required.", "danger")
        existing = ShortenedURL.query.filter(ShortenedURL.short == request.form['short']).first()
        if existing is None:
            nshort = ShortenedURL(short=request.form['short'], longer="/u/%s/projects/%s" % (session['username'], request.form['long']))
            db_session.add(nshort)
            db_session.commit()
            flash("Your link was shortened: http://www.codesphere.org/p/%s" % (request.form['short']), "success")
            #return redirect('/p/%s' % request.form['short'])
        else:
            flash("Sorry, but that short link is already taken.", "danger")
    return render_template('shortener.html')
