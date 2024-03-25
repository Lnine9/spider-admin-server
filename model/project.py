from peewee import DateTimeField, CharField, BigIntegerField, IntegerField, SQL, ForeignKeyField
from model.subject import Subject

from model.base import BaseModel


class Project(BaseModel):
    create_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")], null=True)
    end_time = DateTimeField(null=True)
    id = CharField(primary_key=True)
    name = CharField(null=True)
    schedule_id = CharField(null=True)
    slice_size = IntegerField()
    spider_id = IntegerField(null=True)
    start_time = DateTimeField(null=True)
    status = IntegerField()
    subject = ForeignKeyField(column_name='subject_id', field='id', model=Subject, null=True)
    total_crawl = IntegerField(null=True)
    total_resolve = IntegerField(null=True)
    update_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")], null=True)

    class Meta:
        table_name = 'project'
