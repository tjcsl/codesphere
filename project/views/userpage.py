from flask import render_template

def get_userpage(user):
    return render_template('userpage.html')
