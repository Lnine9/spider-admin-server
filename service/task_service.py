from model.task import Task
from model.subject import Subject
from model.project import Project
from model.schedule import Schedule
from utils.id import generate_uuid
from constants.index import TaskStatus, ProjectStatus
import datetime


class TaskService:
    def __init__(self):
        pass

    @classmethod
    def list_task(cls):
        query = Task.select(Task, Subject.name.alias('subject_name')).left_outer_join(Subject).dicts()
        return list(query)

    @classmethod
    def get_task_by_id(cls, id):
        find = Task.select(Task, Subject.name.alias('subject_name')).left_outer_join(Subject).where(
            Task.id == id).dicts().get()
        return find

    @classmethod
    def add_task(cls, task):
        if task.get('project_id') is None:
            task['id'] = generate_uuid()
        Task.create(**task)

    @classmethod
    def update_task(cls, id, new_task):
        local = Task.get(Task.id == id)
        local.name = new_task['name']
        local.save()

    @classmethod
    def delete_task(cls, id):
        local = Task.get(Task.id == id)
        local.delete_instance()

    @classmethod
    def get_task_by_project_id(cls, project_id):
        query = (Task
                 .select(Task, Subject.name.alias('subject_name'), Project.name.alias('project_name'))
                 .left_outer_join(Subject, on=(Task.subject_id == Subject.id))
                 .left_outer_join(Project, on=(Task.project_id == Project.id))
                 .where(Task.project_id == project_id))

        result = {
            'list': query.dicts(),
            'total': query.count()
        }
        return result

    @classmethod
    def update_task_status(cls, id, data):
        task = Task.get(Task.id == id)
        project = Project.get(Project.id == task.project_id)
        is_from_schedule = project.schedule_id is not None
        schedule = None
        if is_from_schedule:
            schedule = Schedule.get(Schedule.id == project.schedule_id)
        tasks = Task.select().where(Task.project_id == project.id)

        task.status = data.get('status')
        if (task.status == TaskStatus.RUNNING) and (task.start_time is None):
            task.start_time = datetime.datetime.now()

        if (task.status == TaskStatus.COMPLETED) and (task.end_time is None):
            task.end_time = datetime.datetime.now()
            if data.get('total_crawl') is not None:
                task.total_crawl = data.get('total_crawl')
                project.total_crawl += data.get('total_crawl')
            if data.get('total_resolve') is not None:
                task.total_resolve = data.get('total_resolve')
                project.total_resolve += data.get('total_resolve')
            if data.get('log_url') is not None:
                task.log_url = f'{task.node_address}{data.get("log_url")}'
            if is_from_schedule:
                if data.get('last_crawl_time') is not None and data.get('last_crawl_time') is not None:
                    last_crawl_time = datetime.datetime.fromtimestamp(data.get('last_crawl_time'))
                    # 当计划没有最后一次抓取到的公告时间，或最后一次晚于当前任务的抓取到的公告时间
                    if schedule.last_crawl_time is None or schedule.last_crawl_time < last_crawl_time:
                        schedule.last_crawl_time = datetime.datetime.fromtimestamp(data.get('last_crawl_time'))
                        schedule.last_crawl_url = data.get('last_crawl_url')

        if task.status == TaskStatus.ERROR:
            task.end_time = datetime.datetime.now()
            project.status = ProjectStatus.HAS_ERROR
            if data.get('log_url') is not None:
                task.log_url = f'{task.node_address}{data.get("log_url")}'

        if all([t.status == TaskStatus.COMPLETED for t in tasks]):
            project.status = ProjectStatus.COMPLETED
            project.end_time = datetime.datetime.now()

        task.save()
        project.save()
        if is_from_schedule:
            schedule.save()
