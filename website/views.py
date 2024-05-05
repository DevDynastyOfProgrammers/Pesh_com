from flask import Blueprint, render_template
import folium
# import osmnx as ox
# import networkx as nx
# from IPython.display import IFrame
from website.work_with_map.create_a_route import new_route

views = Blueprint('views', __name__)

# Временные данные для удобства
map_point = [64.53821631881615, 40.513887405395515]
start_point = [64.54307276785013, 40.51783561706544]
end_point = [64.53672646553242, 40.531611442565925]
test_map_html = 'test_map_html.html'

@views.route('/', methods=['GET', 'POST'])
def mainWindow():

    mapObj = folium.Map(location=map_point, zoom_start=15, width=1850, height=900)
    
    # добавление маршрута на карту
    mapObj = new_route(mapObj, map_point, start_point, end_point)

    # вывод точек интереса
    

    # рендеринг карты
    mapObj.get_root().render()
    header = mapObj.get_root().header.render()
    body_html = mapObj.get_root().html.render()
    script = mapObj.get_root().script.render()
    window_map = render_template('home.html', header=header, 
                            body_html=body_html, script=script)

    # сохраняем html как файл, чтобы легче было смотреть
    mapObj.save(test_map_html)
    with open(test_map_html, 'w') as mapfile:
        mapfile.write(window_map)

    return window_map