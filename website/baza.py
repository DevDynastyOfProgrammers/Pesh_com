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
    image = TextField()
    # organisator = ForeignKeyField(User, backref='events')
    class Meta:
        table_name = 'event'


if __name__ == '__main__':
    # db.create_tables([User, Role, UserRole])
    print(User.get(User.user_id == 4))
    pass