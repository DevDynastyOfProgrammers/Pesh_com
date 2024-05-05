import folium
import osmnx as ox
import networkx as nx

def osmid_to_coords(graph, ids):
    coords = []
    for i in range(1, len(ids)):
        coords.append([graph.nodes[ids[i]]['y'], graph.nodes[ids[i]]['x']])
    return coords

def new_route(mapObj, map_point, start_point, end_point):
    ox.config(log_console=True, use_cache=True)

    G_walk = ox.graph_from_point(map_point, network_type='walk')

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

    return mapObj
