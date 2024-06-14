from flask import Blueprint, render_template, request
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
start_point = [64.54307276785013, 40.51783561706544]
end_point = [64.53672646553242, 40.531611442565925]

# test_map_html = 'test_map_html.html'

@views.route('/', methods=['GET', 'POST'])
def mainWindow():
    
    # добавление маршрута на карту
    new_route(start_point, end_point)

    # вывод точек интереса
    # show_selected_features(tags=None)
    # show_features()
    show_all_features()

    # вывод области прогулки
    optimal_distance = default_speed*walk_duration//3

    show_walking_area(start_point, optimal_distance)
    near_features(start_point, optimal_distance)

    # select_features_for_walk(start_point, optimal_distance, tags=None)
    
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


@app.route("/dir")
def event():
    events = read_events()
    return render_template("spravochnik.html", events=events)


@app.route("/xu", methods=["GET"])
def event_info():
    event_id = request.args.get("id")
    event = get_event_by_id(event_id)
    place = event.place
    return render_template("info.html", event=event, place=place)
