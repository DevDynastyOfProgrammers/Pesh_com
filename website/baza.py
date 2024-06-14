from peewee import *
import datetime

db = PostgresqlDatabase('neondb', host='ep-bitter-wind-a2twehp1.eu-central-1.aws.neon.tech', port=5432,
                        user='neondb_owner', password='9kuNsG0jbvhe')


class BaseModel(Model):
    class Meta:
        database = db


class Place(BaseModel):
    place_id = AutoField()
    name = TextField(null=False, unique=True)
    description = TextField()
    class Meta:
        table_name = 'place'


class Event(BaseModel):
    event_id = AutoField()
    name = TextField(null=False, unique=True)
    start_date = DateField(default=datetime.date.today)
    end_date = DateField(default=datetime.date.today)
    place = ForeignKeyField(Place, backref='events')
    price = IntegerField()
    start_time = TimeField()
    type = TextField(null=False, unique=True)
    class Meta:
        table_name = 'event'


if __name__ == '__main__':
    db.create_tables([Place, Event])