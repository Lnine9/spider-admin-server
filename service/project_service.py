from model.project import Project
from model.subject import Subject
from model.schedule import Schedule
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
    def query_project(cls, params):
        query = (Project
                 .select(Project, Subject.name.alias('subject_name'), Schedule.name.alias('schedule_name'))
                 .join(Subject, on=(Project.subject_id == Subject.id))
                 .join(Schedule, on=(Project.schedule_id == Schedule.id))
                 .order_by(Project.create_time.desc())
                 .paginate(int(params.get('page_num')), int(params.get('page_size'))))
        if 'subject_id' in params:
            query = query.where(Project.subject_id == params['subject_id'])
        if 'status' in params:
            query = query.where(Project.status == params['status'])
        if 'name' in params:
            query = query.where(Project.name.contains(params['name']))
        if 'create_time_start' in params:
            query = query.where(Project.create_time >= params['create_time_start'])
        if 'create_time_end' in params:
            query = query.where(Project.create_time <= params['create_time_end'])

        result = {
            'list': query.dicts(),
            'total': query.count()
        }
        return result

    @classmethod
    def get_project_by_id(cls, id):
        find = (Project
                 .select(Project, Subject.name.alias('subject_name'), Schedule.name.alias('schedule_name'))
                 .join(Subject, on=(Project.subject_id == Subject.id))
                 .join(Schedule, on=(Project.schedule_id == Schedule.id))
                 .where(Project.id == id)
                 .dicts().get())
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
        range_start_time = project.get('range_start_time')
        range_end_time = project.get('range_end_time')

        delta = datetime.timedelta(minutes=slice_size)
        # 当时间间隔为0时，直接添加任务
        if delta.total_seconds() == 0:
            task = {
                'id': generate_uuid(),
                'name': f"{project.get('name')}:{format_datetime(range_start_time)}-{format_datetime(range_end_time)}",
                'project_id': project.get('id'),
                'spider_id': project.get('spider_id'),
                'subject_id': project.get('subject_id'),
                'range_start_time': range_start_time,
                'range_end_time': range_end_time,
                'status': TaskStatus.UN_COMPLETED
            }
            TaskService.add_task(task)
            return
        # 当时间间隔大于0时，按时间间隔切分任务
        while range_start_time < range_end_time:
            if range_end_time - range_start_time < MIN_SLICE_DATETIME:
                break
            next_start_time = range_start_time + delta
            task = {
                'id': generate_uuid(),
                'name': f"{project.get('name')}:{format_datetime(range_start_time)}-{format_datetime(next_start_time)}",
                'project_id': project.get('id'),
                'spider_id': project.get('spider_id'),
                'subject_id': project.get('subject_id'),
                'range_start_time': range_start_time,
                'range_end_time': next_start_time,
                'status': TaskStatus.UN_COMPLETED
            }
            TaskService.add_task(task)
            start_time = next_start_time
