from flask import Flask
from website.work_with_map.meta_data import *
from website.work_with_map.create_a_route import init_map
from flask_login import LoginManager

map_point = [64.53821631881615, 40.513887405395515]
all_tags = [
    {'amenity' : 'theatre' },
    {'historic' : True}
]
SECRET_KEY = '3055a30ad5d859ed4708a7c118386e7d0ef19ca8'
login_manager = None

def create_app():
    global login_manager
    app = Flask(__name__)
    app.config['SECRET_KEY'] = SECRET_KEY
    login_manager = LoginManager(app)

    from .views import views

    # map and features initalization
    mapObj, gdfs = init_map(map_point, all_tags)
    a = Map(mapObj, gdfs, map_point, all_tags, all_tags)
    Persistence_Exemplar.serialize(a)

    app.register_blueprint(views, url_prefix='/')
    return app

