from api.subject_api import subject_api
from api.schedule_api import schedule_api

ROUTES = {
    '/api/subject': subject_api,
    '/api/schedule': schedule_api
}


def register_blueprint(app):
    for url, blueprint in ROUTES.items():
        app.register_blueprint(blueprint=blueprint, url_prefix=url)
