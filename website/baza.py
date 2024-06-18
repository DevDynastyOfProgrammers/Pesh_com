from peewee import *
import datetime

db = PostgresqlDatabase('neondb', host='ep-bitter-wind-a2twehp1.eu-central-1.aws.neon.tech', port=5432,
                        user='neondb_owner', password='9kuNsG0jbvhe')


class BaseModel(Model):
    class Meta:
        database = db


class Role(BaseModel):
    role_id = AutoField()
    name = TextField(null=False)
    slug = TextField(null=False, unique=True)
    class Meta:
        table_name = 'role'


class User(BaseModel):
    user_id = AutoField()
    name = TextField(null=False)
    email = TextField(null=False)
    psw = TextField(null=False)
    #? time =  IntegerField(null=False)
    #! event_ids = 
    #? role = ForeignKeyField(Role, backref='users')
    class Meta:
        table_name = 'user'

    def has_role(self, role):
        choosed_role = Role.get_or_none(Role.slug == role)
        user_role = UserRole.select().where(
            (UserRole.user_id == self.user_id) &
            (UserRole.role_id == choosed_role.role_id)).get_or_none()
        return user_role


class UserRole(BaseModel):
    user_id = ForeignKeyField(User, backref='user_roles')
    role_id = ForeignKeyField(Role, backref='user_roles')
    class Meta:
        table_name = 'user_roles'
        primary_key = CompositeKey('user_id', 'role_id')


class Place(BaseModel):
    place_id = AutoField()
    name = TextField(null=False)
    description = TextField()
    longitude = DoubleField()
    latitude = DoubleField()
    # start_date = DateField()
    website = TextField()
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
    image = TextField()
    # description = TextField()
    # organisator = ForeignKeyField(User, backref='events')
    class Meta:
        table_name = 'event'


class Connection(BaseModel):
    connection_id = AutoField()
    start_point = ForeignKeyField(Place, backref='places')
    end_point = ForeignKeyField(Place, backref='places')
    class Meta:
        table_name = 'connection'


class Route(BaseModel):
    route_id = AutoField()
    name = TextField(null=False)
    description = TextField()
    class Meta:
        table_name = 'route'


class RouteConnection(BaseModel):
    route_id = ForeignKeyField(Route, backref='route_connections')
    connection_id = ForeignKeyField(Connection, backref='route_connections')
    class Meta:
        table_name = 'route_connection'
        primary_key = CompositeKey('route_id', 'connection_id')

class UserRoute(BaseModel):
    user_id = ForeignKeyField(User, backref='user_routes')
    route_id = ForeignKeyField(Route, backref='user_routes')
    class Meta:
        table_name = 'user_route'
        primary_key = CompositeKey('user_id', 'route_id')



if __name__ == '__main__':
    db.create_tables([UserRoute])
    # print(User.get(User.user_id == 4))