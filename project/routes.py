from project import app
from project.views import core, bugs, links, projects, userpage, chat, whiteboard

def add_url_routes(routes_tuple):
    for route, view_function in routes_tuple:
        app.add_url_rule(route, view_function.__name__, view_function, methods=["GET", "POST"])

add_url_routes((
    ('/', core.index),
    ('/about/', core.about),
    ('/link/<id>/', links.resolve),
    ('/login/', core.login),
    ('/ghcallback/', core.ghcallback),
    ('/logout/', core.logout),
    ('/u/<user>/', userpage.get_userpage),
    ('/u/<user>/projects/', projects.list_projects),
    ('/u/<user>/projects/<project>/', projects.display_project),
    ('/u/<user>/projects/<project>/bugs/', bugs.browse),
    ('/u/<user>/projects/<project>/bugs/new', bugs.new),
    ('/u/<user>/projects/<project>/bugs/view/<id>', bugs.view_bug),
    ('/u/<user>/projects/<project>/import/', projects.import_project),
    ('/u/<user>/projects/<project>/chat/', chat.chat),
    ('/u/<user>/projects/<project>/get_priv_test/', projects.privtest),
    ('/u/<user>/projects/<project>/whiteboard/view/', whiteboard.view_notes),
    ('/u/<user>/projects/<project>/whiteboard/edit/', whiteboard.edit_notes),
    ('/shorten/', links.shortener),
    ('/p/<id>', links.resolve),
    ('/tasks/<int:pid>/task/add/', whiteboard.add_task),
    ('/tasks/<int:pid>/task/del/', whiteboard.del_task)
))
