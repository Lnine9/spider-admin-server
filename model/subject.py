from peewee import *
from .base import BaseModel


class Subject(BaseModel):
    id = CharField(primary_key=True)
    name = CharField()
    description = CharField()
    url = CharField()

    class Meta:
        table_name = 'subject'
