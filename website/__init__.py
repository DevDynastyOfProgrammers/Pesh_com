from flask import Flask
from website.work_with_map.objects import *
from website.work_with_map.create_a_route import init_map
import folium

map_point = [64.53821631881615, 40.513887405395515]
all_tags = [
    {'amenity' : 'theatre' },
    {'historic' : True}
]

def create_app():
    app = Flask(__name__)

    from .views import views

    # map and features initalization
    mapObj, gdfs = init_map(map_point, all_tags)
    a = Map(mapObj, gdfs, map_point, all_tags, all_tags)
    Persistence_Exemplar.serialize(a)

    app.register_blueprint(views, url_prefix='/')
    return app

