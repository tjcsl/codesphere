from project import app
from project.views import core, bugs, links
>>>>>>> Stashed changes

def add_url_routes(routes_tuple):
    for route, view_function in routes_tuple:
        app.add_url_rule(route, view_function.__name__, view_function)

add_url_routes((
    ('/', core.index),
    ('/about/', core.about),
    ('/<owner>/<project>/bugs/', bugs.browse),
    ('/link/<id>', links.resolve),
    ('/login', core.login),
    ('/ghcallback/', core.ghcallback),
    ('/logout', core.logout),
    ('/test', core.temp_test)
    ('/<user>/projects/', projects.list_projects),
    ('/<user>/<project_name>/import/', projects.import_project)
))
