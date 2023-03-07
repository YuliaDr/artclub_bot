from peewee import *

mysql_db = MySQLDatabase('art_bot', user='root', password='',
                         host='localhost', port=3307)


class BaseModel(Model):
    class Meta:
        database = mysql_db


class User(BaseModel):
    id = IntegerField(primary_key=True)
    first_name = CharField()
    last_name = CharField()
    is_admin = BooleanField(default=0)
