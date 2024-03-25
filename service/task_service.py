from model.task import Task
from model.subject import Subject
from utils.id import generate_uuid


class TaskService:
    def __init__(self):
        pass

    @classmethod
    def list_task(cls):
        query = Task.select(Task, Subject.name.alias('subject_name')).join(Subject).dicts()
        return list(query)

    @classmethod
    def get_task_by_id(cls, id):
        find = Task.select(Task, Subject.name.alias('subject_name')).join(Subject).where(Task.id == id).dicts().get()
        return find

    @classmethod
    def add_task(cls, task):
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

