import time

from peewee import *
from playhouse.pool import PooledMySQLDatabase
from playhouse.shortcuts import ReconnectMixin

from setting import MYSQL

class ReconnectPooledMySQLDatabase(ReconnectMixin, PooledMySQLDatabase):
    _instance = None

    @classmethod
    def get_db_instance(cls):
        if not cls._instance:
            cls._instance = cls(MYSQL['DB'],
                                max_connections=10,
                                stale_timeout=300,
                                host=MYSQL['HOST'],
                                port=MYSQL['PORT'],
                                user=MYSQL['USER'],
                                password=MYSQL['PASSWORD'])
        return cls._instance
# 数据库实例
db = ReconnectPooledMySQLDatabase.get_db_instance()

class BaseModel(Model):
    class Meta:
        database = db


