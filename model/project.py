from peewee import DateTimeField, CharField, IntegerField, SQL
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
    subject_id = CharField(null=True)
    total_crawl = IntegerField(null=True)
    total_resolve = IntegerField(null=True)
    update_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")], null=True)
    range_start_time = DateTimeField(null=True)
    range_end_time = DateTimeField(null=True)
    mode = IntegerField()

    class Meta:
        table_name = 'project'
