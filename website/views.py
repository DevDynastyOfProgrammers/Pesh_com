from flask import Blueprint, render_template
import folium
# import osmnx as ox
# import networkx as nx
# from IPython.display import IFrame
from website.work_with_map.create_a_route import *

views = Blueprint('views', __name__)

# Временные данные для удобства
default_speed = 1.1 * 60    # метров в минуту
walk_duration = 30
map_point = [64.53821631881615, 40.513887405395515]
start_point = [64.54307276785013, 40.51783561706544]
end_point = [64.53672646553242, 40.531611442565925]
tags = [
    {'amenity' : 'theatre' },
    {'historic' : True}
]
test_map_html = 'test_map_html.html'

@views.route('/', methods=['GET', 'POST'])
def mainWindow():

    mapObj = folium.Map(location=map_point, zoom_start=15, width=1850, height=900)
    
    # добавление маршрута на карту
    mapObj = new_route(mapObj, map_point, start_point, end_point)

    # вывод точек интереса
    mapObj = show_selected_features(mapObj, map_point, tags)

    # вывод области прогулки
    optimal_distance = default_speed*walk_duration//3
    folium.Circle(
        location=start_point,
        radius=optimal_distance,
        color="black",
        weight=1,
        fill_opacity=0.6,
        opacity=1,
        fill_color="green",
        fill=False,  # gets overridden by fill_color
        popup="{} meters".format(optimal_distance),
        tooltip="I am in meters",
    ).add_to(mapObj)

    print(optimal_distance)
    mapObj = select_features_for_walk(mapObj, map_point, tags, start_point, optimal_distance)
    
    # рендеринг карты
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