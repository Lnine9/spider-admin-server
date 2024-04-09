from peewee import DateTimeField, CharField, TextField, BigIntegerField, IntegerField, SQL, ForeignKeyField

from model.base import BaseModel


class User(BaseModel):
    id = CharField(primary_key=True)
    user_name = CharField(null=True)
    password = CharField(null=True)
    create_time = DateTimeField(null=True)
    state = IntegerField(null=True)

    class Meta:
        table_name = 'user'
