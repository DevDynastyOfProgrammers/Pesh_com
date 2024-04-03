from flask import Blueprint, render_template
import folium
import osmnx as ox
import networkx as nx
from IPython.display import IFrame

views = Blueprint('views', __name__)

start_point = [64.54307276785013, 40.51783561706544]
end_point = [64.53672646553242, 40.531611442565925]

def OsmidToCoords(graph, ids):
    coords = []
    for i in range(1, len(ids)):
        coords.append([graph.nodes[ids[i]]['y'], graph.nodes[ids[i]]['x']])
    return coords

def FindPopUpSlice(html):
    '''
    Find the starting and ending index of popup function
    '''

    pattern = 'function latLngPop(e)'

    # starting index
    starting_index = html.find(pattern)
    # ending_index = html[starting_index:].find('}')
    закончил здесь

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
        locations=OsmidToCoords(G_walk, route)
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

    def CreatePopUp(html):
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
    
    CreatePopUp(window_map)

    mapObj.save(test_map_html)

    return window_map