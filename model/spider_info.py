from peewee import DateTimeField, CharField, BigIntegerField, IntegerField, SQL, ForeignKeyField, BitField, TextField

from model.base import BaseModel


class SpiderInfo(BaseModel):
    id = CharField(primary_key=True)
    name = CharField(null=True)
    model_id = CharField(null=True)
    an_type = CharField(null=True)
    enable = IntegerField()
    description = CharField()
    section_page_size = IntegerField()
    callback = CharField(null=True)
    method = CharField(null=True)
    body = TextField()
    url = TextField()
    resolvers = TextField()
    main_class = CharField()

    class Meta:
        table_name = 'spider_info'
