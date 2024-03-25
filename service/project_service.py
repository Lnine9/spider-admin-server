from model.project import Project
from model.subject import Subject
from utils.id import generate_uuid
import datetime
from utils.time_util import format_datetime
from constants.index import ProjectStatus, TaskStatus
from service.task_service import TaskService

MIN_SLICE = 10
MIN_SLICE_DATETIME = datetime.timedelta(minutes=MIN_SLICE)

class ProjectService:
    def __init__(self):
        pass

    @classmethod
    def list_project(cls):
        query = Project.select(Project, Subject.name.alias('subject_name')).join(Subject).dicts()
        return list(query)

    @classmethod
    def get_project_by_id(cls, id):
        find = Project.select(Project, Subject.name.alias('subject_name')).join(Subject).where(Project.id == id).dicts().get()
        return find

    @classmethod
    def add_project(cls, project):
        project['id'] = generate_uuid()
        Project.create(**project)

        cls.split_project(project)

    @classmethod
    def update_project(cls, id, new_project):
        local = Project.get(Project.id == id)
        local.name = new_project['name']
        local.schedule_id = new_project['schedule_id']
        local.slice_size = new_project['slice_size']
        local.status = new_project['status']
        local.start_time = new_project['start_time']
        local.end_time = new_project['end_time']
        local.save()

    @classmethod
    def delete_project(cls, id):
        local = Project.get(Project.id == id)
        local.delete_instance()

    @classmethod
    def split_project(cls, project):
        slice_size = project.get('slice_size')
        start_time = project.get('start_time')
        end_time = project.get('end_time')

        delta = datetime.timedelta(minutes=slice_size)
        # 当时间间隔为0时，直接添加任务
        if delta.total_seconds() == 0:
            task = {
                'id': generate_uuid(),
                'name': f"{project.get('name')}:{format_datetime(start_time)}-{format_datetime(end_time)}",
                'project_id': project.get('id'),
                'spider_id': project.get('spider_id'),
                'subject_id': project.get('subject_id'),
                'start_time': start_time,
                'end_time': end_time,
                'status': TaskStatus.UN_COMPLETED
            }
            TaskService.add_task(task)
            return
        # 当时间间隔大于0时，按时间间隔切分任务
        while start_time < end_time:
            if end_time - start_time < MIN_SLICE_DATETIME:
                break
            next_start_time = start_time + delta
            task = {
                'id': generate_uuid(),
                'name': f"{project.get('name')}:{format_datetime(start_time)}-{format_datetime(next_start_time)}",
                'project_id': project.get('id'),
                'spider_id': project.get('spider_id'),
                'subject_id': project.get('subject_id'),
                'start_time': start_time,
                'end_time': next_start_time,
                'status': TaskStatus.UN_COMPLETED
            }
            TaskService.add_task(task)
            start_time = next_start_time

