from api.login_api import login_api
from api.spider_api import spider_api
from api.subject_api import subject_api
from api.schedule_api import schedule_api
from api.project_api import project_api
from api.task_api import task_api

ROUTES = {
    '/api/subject': subject_api,
    '/api/schedule': schedule_api,
    '/api/sign': login_api,
    '/api/project': project_api,
    '/api/task': task_api,
    '/api/spider': spider_api,
}


def register_blueprint(app):
    for url, blueprint in ROUTES.items():
        app.register_blueprint(blueprint=blueprint, url_prefix=url)
