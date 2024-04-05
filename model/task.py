from peewee import DateTimeField, CharField, TextField, BigIntegerField, IntegerField, SQL, ForeignKeyField
from model.subject import Subject

from model.base import BaseModel


class Task(BaseModel):
    create_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")], null=True)
    end_time = DateTimeField(null=True)
    id = CharField(primary_key=True)
    job_id = CharField(null=True)
    log_url = TextField(null=True)
    project_id = CharField(null=True)
    spider_id = CharField(null=True)
    start_time = DateTimeField(null=True)
    status = IntegerField()
    subject_id = CharField(null=True)
    total_crawl = IntegerField(null=True)
    total_resolve = IntegerField(null=True)
    update_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")], null=True)
    range_start_time = DateTimeField(null=True)
    range_end_time = DateTimeField(null=True)

    class Meta:
        table_name = 'task'
