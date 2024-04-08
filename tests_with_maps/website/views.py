from flask import Blueprint, render_template
import folium
import osmnx as ox
import networkx as nx
from IPython.display import IFrame

views = Blueprint('views', __name__)

start_point = [64.54307276785013, 40.51783561706544]
end_point = [64.53672646553242, 40.531611442565925]

def osmid_to_coords(graph, ids):
    coords = []
    for i in range(1, len(ids)):
        coords.append([graph.nodes[ids[i]]['y'], graph.nodes[ids[i]]['x']])
    return coords

def find_popup_slice(html):
    '''
    вводим html странницы в виде строки и находим начальный и конечный индексы функции popup.
    нужна для инъекции.
    '''

    pattern = 'function latLngPop(e) {'
    
    starting_index = html.find(pattern)
    tmp_html = html[starting_index + len(pattern):]
    
    is_opened = 1
    index = 0
    while is_opened > 0:
        if tmp_html[index] == "{":
            is_opened += 1
        elif tmp_html[index] == "}":
            is_opened -= 1

        index += 1
    ending_index = starting_index + len(pattern) + index
    
    return starting_index, ending_index

def find_varieble_name(html, start_pattern):
    """
    находим название карты
    """
    end_pattern = ' ='
    
    starting_index = html.find(start_pattern) + 4 # игнорируем 'var '
    tmp_html = html[starting_index:]
    ending_index = tmp_html.find(end_pattern) + starting_index
    return html[starting_index:ending_index]

def custom_code(map_variable_name, popup_variable_name):
    return '''
    // custom code
    function latLngPop(e) {
        %s
            .setLatLng(e.latlng)
            .setContent("Latitude: " + e.latlng.lat.toFixed(4) +
                        "<br>Longitude: " + e.latlng.lng.toFixed(4))
            .openOn(%s);
        
        console.log("Latitude: " + e.latlng.lat.toFixed(4));
        console.log("Longitude: " + e.latlng.lng.toFixed(4));
        }
    // end custom code
    ''' % (popup_variable_name, map_variable_name)

@views.route('/', methods=['GET', 'POST'])
def mainWindow():
    test_map_html = 'test_map_html.html'

    mapObj = folium.Map(location=[64.53821631881615, 40.513887405395515], zoom_start=15, width=1850, height=900)
    
    ox.config(log_console=True, use_cache=True)

    G_walk = ox.graph_from_point((64.53821631881615, 40.513887405395515),
                            network_type='walk')
    
    orig_node = ox.nearest_nodes(G_walk, Y=start_point[0], X=start_point[1])
    dest_node = ox.nearest_nodes(G_walk, Y=end_point[0], X=end_point[1])

    # создание маршрута
    route = nx.shortest_path(G_walk,
                            orig_node,
                            dest_node,
                            weight='length')
    
    # добавление маршрута на карту
    folium.PolyLine(
        locations=osmid_to_coords(G_walk, route)
    ).add_to(mapObj)

    """обучение"""
    def CreateMarkersLines():
        line_coords = [
            start_point,
            end_point
        ]
        folium.Marker(
            location=start_point,
            tooltip="I am the start!"
        ).add_to(mapObj)
        
        folium.PolyLine(
            line_coords,
            color="red",
            weight="10",
            opacity=0.5
        ).add_to(mapObj)

        polygon_coords = [
            [64.54225626680378, 40.53488864633583],
            [64.5408545380799, 40.52443888670781],
            [64.53824066116553, 40.539728841630996],
            [64.54225626680378, 40.53488864633583]
        ]

        polygon_lines = [
            [polygon_coords[i], polygon_coords[i+1]] for i in range(len(polygon_coords) - 1)
        ]

        # создаем треугольник по 4 точкам
        # folium.PolyLine(
        #     polygon_coords,
        #     color="red",
        #     weight="10",
        #     opacity=0.5
        # ).add_to(mapObj)

        # создаем треугольник по 3 линиям
        for line in polygon_lines:
            folium.PolyLine(
                line,
                color="red",
                weight="10",
                opacity=0.5
            ).add_to(mapObj)

    # тестовая штука
    folium.LatLngPopup().add_to(mapObj)
    

    # render the map object
    mapObj.get_root().render()

    # derive the script and style tags to be rendered in HTML head
    header = mapObj.get_root().header.render()

    # derive the div container to be rendered in the HTML body
    body_html = mapObj.get_root().html.render()

    # derive the JavaScript to be rendered in the HTML body
    script = mapObj.get_root().script.render()

    window_map = render_template('home.html', header=header, 
                            body_html=body_html, script=script)

    pstart, pend = find_popup_slice(window_map)
    # print(window_map[pstart:pend])
    # print(find_map_varieble_name(window_map))
    # print(find_popup_varieble_name(window_map))

    # inject custom code
    window_map = window_map[:pstart] + \
    custom_code(find_varieble_name(window_map, 'var map_'), find_varieble_name(window_map, 'var lat_lng_popup_')) + \
    window_map[pend:]

    # сохраняем html как файл, чтобы легче было смотреть
    mapObj.save(test_map_html)
    with open(test_map_html, 'w') as mapfile:
        mapfile.write(window_map)

    return window_map