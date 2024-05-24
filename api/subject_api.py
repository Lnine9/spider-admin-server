from utils.flask_ext.flask_app import BlueprintAppApi
from service.subject_service import SubjectService
from flask import request

subject_api = BlueprintAppApi(name="subject", import_name=__name__)


@subject_api.get('/list')
def list_subject():
    return SubjectService.list_subject()


@subject_api.get('/get')
def get_subject_by_id():
    id = request.args.get('id')
    return SubjectService.get_subject_by_id(id)


@subject_api.post('/add')
def add_subject():
    name = request.json.get('name')
    description = request.json.get('description')
    url = request.json.get('url')
    subject = {
        'name': name,
        'description': description,
        'url': url
    }
    return SubjectService.add_subject(subject)


@subject_api.post('/update')
def update_subject():
    id = request.json.get('id')
    return SubjectService.update_subject(id, request.json)


@subject_api.post('/delete')
def delete_subject():
    id = request.json.get('id')
    return SubjectService.delete_subject(id)
