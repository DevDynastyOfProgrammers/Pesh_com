from flask import Blueprint, render_template
from flask_login import current_user
import folium
import osmnx as ox
import networkx as nx
from .map_initialize import G_walk
from IPython.display import IFrame

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
def traffic_controller():

    # ox.config(log_console=True, use_cache=True)

    # G_walk = ox.graph_from_place('Manhattan Island, New York City, New York, USA',
    #                         network_type='walk')
    
    # orig_node = ox.nearest_nodes(G_walk, Y=40.748441, X=-73.985664)

    # dest_node = ox.nearest_nodes(G_walk, Y=40.748441, X=-73.3)

    # route = nx.shortest_path(G_walk,
    #                         orig_node,
    #                         dest_node,
    #                         weight='length')

    # mapObj = ox.plot_route_folium(G_walk, route)
    # print()
    # print(type(mapObj), type(folium.Map(location=[64.5383, 40.5140],
    #                     zoom_start=17, width=1850, height=910)))
    # print()


    mapObj = folium.Map(location=[64.5383, 40.5140],
                        zoom_start=17, width=1850, height=910)

    # render the map object
    mapObj.get_root().render()

    # derive the script and style tags to be rendered in HTML head
    header = mapObj.get_root().header.render()

    # derive the div container to be rendered in the HTML body
    body_html = mapObj.get_root().html.render()

    # derive the JavaScript to be rendered in the HTML body
    script = mapObj.get_root().script.render()

    print(header, body_html, script)

    return render_template('home.html', user=current_user, 
                        header=header, body_html=body_html, script=script)