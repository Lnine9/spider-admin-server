from utils.flask_ext.flask_app import BlueprintAppApi
from service.schedule_service import ScheduleService
from flask import request

schedule_api = BlueprintAppApi(name="schedule", import_name=__name__)


@schedule_api.get("/list")
def list_schedule():
    params = request.args.to_dict()
    return ScheduleService.list_schedule(params)


@schedule_api.get("/get")
def get_schedule_by_id():
    id = request.args.get('id')
    return ScheduleService.get_schedule_by_id(id)


@schedule_api.post("/add")
def add_schedule():
    name = request.json.get('name')
    description = request.json.get('description')
    cron = request.json.get('cron')
    slice_size = request.json.get('slice_size')
    spider_id = request.json.get('spider_id')
    subject_id = request.json.get('subject_id')
    schedule = {
        'name': name,
        'description': description,
        'cron': cron,
        'slice_size': slice_size,
        'spider_id': spider_id,
        'subject_id': subject_id
    }
    return ScheduleService.add_schedule(schedule)


@schedule_api.post("/update")
def update_schedule():
    id = request.json['id']
    name = request.json.get('name')
    cron = request.json.get('cron')
    slice_size = request.json.get('slice_size')
    description = request.json.get('description')
    schedule = {
        'name': name,
        'cron': cron,
        'slice_size': slice_size,
        'description': description
    }
    return ScheduleService.update_schedule(id, schedule)


@schedule_api.post("/delete")
def delete_schedule():
    id = request.json.get('id')
    return ScheduleService.delete_schedule(id)


@schedule_api.post("/changeStatus")
def change_status():
    id = request.json.get('id')
    status = request.json.get('status')
    return ScheduleService.change_status(id, status)

