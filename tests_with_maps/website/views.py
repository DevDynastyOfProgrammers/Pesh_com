from flask import Blueprint, render_template
import folium
import osmnx as ox
import networkx as nx
from IPython.display import IFrame

views = Blueprint('views', __name__)

def OsmidToCoords(graph, ids):
    coords = []
    for i in range(1, len(ids)):
        coords.append([graph.nodes[ids[i]]['y'], graph.nodes[ids[i]]['x']])
    return coords

@views.route('/', methods=['GET', 'POST'])
def traffic_controller():
    
    # test_dir = "mapObj.html"
    # check_dir = "osmnx.html"
    mapObj = folium.Map(location=[64.53821631881615, 40.513887405395515], zoom_start=15, width=1850, height=900)
    
    ox.config(log_console=True, use_cache=True)

    G_walk = ox.graph_from_point((64.53821631881615, 40.513887405395515),
                            network_type='walk')
    
    orig_node = ox.nearest_nodes(G_walk, Y=64.54307276785013, X=40.51783561706544)
    dest_node = ox.nearest_nodes(G_walk, Y=64.53672646553242, X=40.531611442565925)

    route = nx.shortest_path(G_walk,
                            orig_node,
                            dest_node,
                            weight='length')
    osmnx_map = ox.plot_route_folium(G_walk, route)

    folium.PolyLine(
        locations=OsmidToCoords(G_walk, route)
    ).add_to(mapObj)

    # mapObj.save(test_dir)
    # osmnx_map.save(check_dir)


    # render the map object
    mapObj.get_root().render()

    # derive the script and style tags to be rendered in HTML head
    header = mapObj.get_root().header.render()

    # derive the div container to be rendered in the HTML body
    body_html = mapObj.get_root().html.render()

    # derive the JavaScript to be rendered in the HTML body
    script = mapObj.get_root().script.render()

    return render_template('home.html', header=header, 
                            body_html=body_html, script=script)