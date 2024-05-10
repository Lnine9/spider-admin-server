from peewee import DateTimeField, CharField, BigIntegerField, IntegerField, SQL, ForeignKeyField, BitField, TextField

from model.base import BaseModel


class Resolver(BaseModel):
    id = IntegerField(primary_key=True)
    name = CharField(null=True)
    type = CharField()
    class_path = TextField(null=True)
    discription = TextField(null=True)
    priority = IntegerField(null=True)
    version_no = CharField()

    class Meta:
        table_name = 'resolver'
