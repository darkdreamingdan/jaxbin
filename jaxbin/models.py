from peewee import *
from . import config
import datetime

db = MySQLDatabase(host=config.db_host, user=config.db_user, password=config.db_password, database=config.db_name)

class BaseModel(Model):
    class Meta:
        database = db

class Bin(BaseModel):
    p_id = CharField(unique=True)
    content = TextField()
    created_date = DateTimeField(default=datetime.datetime.now)
