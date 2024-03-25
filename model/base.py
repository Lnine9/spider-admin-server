from peewee import *
from setting import MYSQL

db = MySQLDatabase(MYSQL['DB'], host=MYSQL['HOST'], port=MYSQL['PORT'], user=MYSQL['USER'], password=MYSQL['PASSWORD'])
db.connect()

class BaseModel(Model):
    class Meta:
        database = db


