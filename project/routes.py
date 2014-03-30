from project import app
from project.views import core, bugs, links, projects, userpage, chat

def add_url_routes(routes_tuple):
    for route, view_function in routes_tuple:
        app.add_url_rule(route, view_function.__name__, view_function)

add_url_routes((
    ('/', core.index),
    ('/about/', core.about),
    ('/link/<id>/', links.resolve),
    ('/login/', core.login),
    ('/ghcallback/', core.ghcallback),
    ('/logout/', core.logout),
    ('/test/', core.temp_test),
    ('/u/<user>/', userpage.get_userpage),
    ('/u/<user>/projects/', projects.list_projects),
    ('/u/<user>/projects/<project>/bugs/', bugs.browse),
    ('/u/<user>/projects/<project>/import/', projects.import_project),
    ('/u/<user>/projects/<project>/chat/', chat.chat),
    ('/p/<id>/', links.resolve),
    ('/shorten/', links.shortener)
))
