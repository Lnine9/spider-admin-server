from utils.flask_ext.flask_app import BlueprintAppApi
from service.project_service import ProjectService
from flask import request
from utils.index import clean_params
from constants.index import ProjectStatus, TaskMode
import datetime

project_api = BlueprintAppApi(name="project", import_name=__name__)


@project_api.get('/query')
def query_project():
    params = clean_params(request.args.to_dict())
    return ProjectService.query_project(params)


@project_api.get('/get')
def get_project_by_id():
    id = request.args.get('id')
    return ProjectService.get_project_by_id(id)


@project_api.post('/add')
def add_project():
    name = request.json.get('name')
    subject_id = request.json.get('subject_id')
    schedule_id = request.json.get('schedule_id')
    slice_size = request.json.get('slice_size')
    range_start_time = datetime.datetime.fromtimestamp(request.json.get('range_start_time'))
    range_end_time = datetime.datetime.fromtimestamp(request.json.get('range_end_time'))
    project = {
        'name': name,
        'subject_id': subject_id,
        'schedule_id': schedule_id,
        'slice_size': slice_size,
        'status': ProjectStatus.UN_COMPLETED,
        'range_start_time': range_start_time,
        'range_end_time': range_end_time,
        'mode': TaskMode.RANGE,
    }
    return ProjectService.add_project(project)


@project_api.post('/update')
def update_project():
    id = request.json['id']
    name = request.json.get('name')
    schedule_id = request.json.get('schedule_id')
    slice_size = request.json.get('slice_size')
    status = request.json.get('status')
    start_time = request.json.get('start_time')
    end_time = request.json.get('end_time')
    project = {
        'name': name,
        'schedule_id': schedule_id,
        'slice_size': slice_size,
        'status': status,
        'start_time': start_time,
        'end_time': end_time
    }
    return ProjectService.update_project(id, project)


@project_api.post('/delete')
def delete_project():
    id = request.json.get('id')
    return ProjectService.delete_project(id)
