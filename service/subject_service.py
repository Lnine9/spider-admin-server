from model.subject import Subject
from utils.id import generate_uuid
from playhouse.shortcuts import model_to_dict


class SubjectService:
    def __init__(self):
        pass

    @classmethod
    def list_subject(cls):
        query = Subject.select()
        return list(query)

    @classmethod
    def get_subject_by_id(cls, id):
        return model_to_dict(Subject.get(Subject.id == id))

    @classmethod
    def add_subject(cls, subject):
        subject['id'] = generate_uuid()
        Subject.create(**subject)

    @classmethod
    def update_subject(cls, id, new_subject):
        local = Subject.get(Subject.id == id)
        local.name = new_subject['name']
        local.description = new_subject['description']
        local.save()

    @classmethod
    def delete_subject(cls, id):
        local = Subject.get(Subject.id == id)
        local.delete_instance()
