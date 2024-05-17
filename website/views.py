from flask import Blueprint, render_template
import folium
# import osmnx as ox
# import networkx as nx
# from IPython.display import IFrame
from website.work_with_map.create_a_route import *
from website.work_with_map.objects import Persistence_Exemplar

views = Blueprint('views', __name__)

# Временные данные для удобства
default_speed = 1.1 * 60    # метров в минуту
walk_duration = 30
# map_point = [64.53821631881615, 40.513887405395515]
start_point = [64.54307276785013, 40.51783561706544]
end_point = [64.53672646553242, 40.531611442565925]
# all_tags = [
#     {'amenity' : 'theatre' },
#     {'historic' : True}
# ]
# test_map_html = 'test_map_html.html'

@views.route('/', methods=['GET', 'POST'])
def mainWindow():
    
    # добавление маршрута на карту
    new_route(start_point, end_point)

    # вывод точек интереса
    show_selected_features(tags=None)

    # вывод области прогулки
    optimal_distance = default_speed*walk_duration//3

    show_walking_area(start_point, optimal_distance)

    select_features_for_walk(start_point, optimal_distance, tags=None)
    
    # рендеринг карты
    mapObj = Persistence_Exemplar.deserialize().mapObj
    mapObj.get_root().render()
    header = mapObj.get_root().header.render()
    body_html = mapObj.get_root().html.render()
    script = mapObj.get_root().script.render()
    window_map = render_template('home.html', header=header, 
                            body_html=body_html, script=script)

    # сохраняем html как файл, чтобы просмотреть весь код страницы
    # mapObj.save(test_map_html)
    # with open(test_map_html, 'w') as mapfile:
    #     mapfile.write(window_map)

    return window_map