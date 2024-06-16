from flask import Flask
from website.work_with_map.meta_data import *
from website.work_with_map.create_a_route import init_map_data
from website.baza import *
from flask_login import LoginManager

from flask_admin import Admin, BaseView, expose, AdminIndexView
from flask_admin.contrib.peewee import ModelView

map_point = [64.53821631881615, 40.513887405395515]
all_tags = [
    {'amenity' : 'theatre' },
    {'historic' : True}
]
SECRET_KEY = '3055a30ad5d859ed4708a7c118386e7d0ef19ca8'
login_manager = None


class ReturnAdminPage(BaseView):
    @expose('/')
    def return_to_main(self):
        return self.render('admin/return.html')


def create_app():
    global login_manager
    app = Flask(__name__)
    app.config['SECRET_KEY'] = SECRET_KEY
    app.config['FLASK_ENV'] = 'development'
    login_manager = LoginManager(app)
    login_manager.login_view = 'views.login'
    login_manager.login_message = u"Авторизуйтесь для доступа к закрытым страницам"
    login_manager.login_message_category = "success"

    admin = Admin(app, name='Администратор', template_mode='bootstrap3')
    admin.add_view(ModelView(User, name='Пользователи'))
    admin.add_view(ModelView(Role, name='Роли'))
    admin.add_view(ModelView(UserRole, name='Роль-Пользователи'))
    admin.add_view(ModelView(Event, name='Мероприятия'))
    admin.add_view(ModelView(Place, name='Места'))
    admin.add_view(ReturnAdminPage(name='Вернуться'))


    from .views import views

    # map and features initalization
    mapObj, gdfs = init_map_data(map_point, all_tags)
    meta = Map(mapObj, gdfs, map_point, all_tags, all_tags)
    Persistence_Exemplar.serialize(meta)

    app.register_blueprint(views, url_prefix='/')
    return app

