from peewee import DateTimeField, CharField, BigIntegerField, IntegerField, SQL, ForeignKeyField
from model.subject import Subject

from model.base import BaseModel


class Schedule(BaseModel):
    create_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")], null=True)
    cron = CharField(null=True)
    id = CharField(primary_key=True)
    name = CharField(null=True)
    description = CharField(null=True)
    slice_size = IntegerField()
    spider_id = CharField(null=True)
    status = IntegerField()
    subject_id = CharField(null=True)
    update_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")], null=True)
    last_run_time = DateTimeField(null=True)

    class Meta:
        table_name = 'schedule'
