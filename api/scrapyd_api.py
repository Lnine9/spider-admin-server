from utils.flask_ext.flask_app import BlueprintAppApi
from service.scrapyd_service import ScrapydService
from flask import request

scrapyd_api = BlueprintAppApi(name="scrapyd", import_name=__name__)


@scrapyd_api.get('/list')
def list_scrapyd_node():
    return ScrapydService.list_scrapyd_node()


@scrapyd_api.get('/detail')
def get_node_detail():
    id = request.args.get('id')
    return ScrapydService.get_node_detail(id)


@scrapyd_api.post('/add')
def add_node():
    return ScrapydService.add_node(request.json)


@scrapyd_api.post('/delete')
def delete_node():
    id = request.json.get('id')
    return ScrapydService.delete_node(id)


@scrapyd_api.post('/refresh')
def refresh():
    return ScrapydService.connect_nodes()

