from peewee import DateTimeField, CharField, BigIntegerField, IntegerField, SQL, ForeignKeyField, BitField, TextField
from model.subject import Subject

from model.base import BaseModel


class SpiderInfo(BaseModel):
    id = CharField(primary_key=True)
    code = CharField(null=True)
    name = CharField(null=True)
    model_id = CharField(null=True)
    an_type = CharField(null=True)
    enable = BitField()
    discription = CharField()
    status = IntegerField()
    section_page_size = IntegerField()
    callback = CharField(null=True)
    method = CharField(null=True)
    body = TextField()
    base_url =CharField()

    class Meta:
        table_name = 'spider_info'
