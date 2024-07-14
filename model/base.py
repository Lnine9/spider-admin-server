from peewee import *
from playhouse.pool import PooledMySQLDatabase

from setting import MYSQL

db = PooledMySQLDatabase(MYSQL['DB'],
                         max_connections=10,
                         stale_timeout=300,
                         host=MYSQL['HOST'],
                         port=MYSQL['PORT'],
                         user=MYSQL['USER'],
                         password=MYSQL['PASSWORD'])
db.connect()

class BaseModel(Model):
    class Meta:
        database = db


