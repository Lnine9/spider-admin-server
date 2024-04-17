from peewee import CharField, IntegerField
from model.base import BaseModel


class ScrapydNode(BaseModel):
    id = IntegerField(primary_key=True)
    name = CharField()
    address = CharField()

    class Meta:
        table_name = 'scrapyd_nodes'
