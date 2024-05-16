import folium
import numpy as np
import osmnx as ox
import networkx as nx
import pandas as pd
import geopandas as gpd
import math

# Вспомогательные функции

def _osmid_to_coords(graph, ids):
    """
    Вывод координат объекта по его ID в OSM
    """
    coords = []
    for i in range(1, len(ids)):
        coords.append([graph.nodes[ids[i]]['y'], graph.nodes[ids[i]]['x']])
    return coords

def _osm_query(tag, map_point):
    """
    Импорт данных объекта/-ов из OSM по 1 тегу.
    """
    gdf = ox.features_from_point(map_point, tag).reset_index()
    gdf['object'] = np.full(len(gdf), list(tag.keys())[0])
    gdf['type'] = np.full(len(gdf), tag[list(tag.keys())[0]])
    gdf = gdf[['name', 'object', 'type', 'geometry']]
    
    return gdf

def _get_point_coords(geometry: "gpd.geoseries.GeoSeries") -> 'tuple':
    """
    Получение координат точки (или центра точек) объекта Point и других
    Использует geopandas.geoseries.GeoSeries (на данный момент это gdf['geometry'])
    Вывод кортеж широты и долготы объекта. Если это полигон, то выводит центрированную точку
    """
    lon = geometry.apply(lambda x: x.x if x.geom_type == 'Point' else x.centroid.x)
    lat = geometry.apply(lambda x: x.y if x.geom_type == 'Point' else x.centroid.y)
    return lat.iloc[0], lon.iloc[0]

def _get_featuters(map_point, tags):
    # в нем будут храниться все объекты
    gdfs = None
    # добавление объектов
    for tag in tags:
        if gdfs is None:
            gdfs = _osm_query(tag, map_point)
        else:
            gdfs = pd.concat([gdfs, _osm_query(tag, map_point)], ignore_index=True)
    return gdfs

def _points_dist(llat1, llong1, llat2, llong2):
    # rad - радиус сферы (Земли)
    rad = 6372795

    #в радианах
    lat1 = llat1*math.pi/180.
    lat2 = llat2*math.pi/180.
    long1 = llong1*math.pi/180.
    long2 = llong2*math.pi/180.

    #косинусы и синусы широт и разницы долгот
    cl1 = math.cos(lat1)
    cl2 = math.cos(lat2)
    sl1 = math.sin(lat1)
    sl2 = math.sin(lat2)
    delta = long2 - long1
    cdelta = math.cos(delta)
    sdelta = math.sin(delta)

    #вычисления длины большого круга
    y = math.sqrt(math.pow(cl2*sdelta,2)+math.pow(cl1*sl2-sl1*cl2*cdelta,2))
    x = sl1*sl2+cl1*cl2*cdelta
    ad = math.atan2(y,x)
    dist = ad*rad

    return dist

# Основные функции

def new_route(mapObj, map_point, start_point, end_point):
    """
    добавляет на карту (mapObj) маршрут по координатам начального и конечного места
    """
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
        locations=_osmid_to_coords(G_walk, route)
    ).add_to(mapObj)

    return mapObj

def show_selected_features(mapObj, map_point, tags):
    """
    вывод точек и полигонов из OSM по выбранным тегам
    """
    # Датафрейм со всеми выбранными объектами
    gdfs = _get_featuters(map_point, tags)

    # добавление каждого объекта на карту
    for gdf_id in range(len(gdfs.values)):
        # берем данные объекта по его id в ГеоДатаФрейме
        gdf = gdfs.iloc[[gdf_id]]
        gdf_type = gdf.geom_type.values[0]

        # добавление объектов на карту и их кастомизация 
        if gdf_type == 'Point':
            gdf_point = gdf.geometry.values[0]
            folium.CircleMarker(
                location=(gdf_point.y, gdf_point.x),
                radius=5,
                color="#3186cc",
                fill=True,
                fill_color="#3186cc"
            ).add_to(mapObj)

        elif gdf_type == 'Polygon':
            sim_geo = gpd.GeoSeries(gdf.geometry.values[0]).simplify(tolerance=0.001)
            geo_j = sim_geo.to_json()
            geo_j = folium.GeoJson(data=geo_j, style_function=lambda x: {"fillColor": "pink"})
            geo_j.add_to(mapObj)
    
    return mapObj


def select_features_for_walk(mapObj, map_point, tags, center, radius):
    # Датафрейм со всеми выбранными объектами
    gdfs = _get_featuters(map_point, tags)

    for gdf_id in range(len(gdfs.values)):
        gdf = gdfs.iloc[[gdf_id]]
        gdf_type = gdf.geom_type.values[0]
        coords = _get_point_coords(gdf['geometry'])

        distance = _points_dist(coords[0], coords[1], center[0], center[1])
        print(distance, radius)
        if distance < radius:
            # print(distance)
            # print(gdf, coords)

            # добавление объектов на карту и их кастомизация 
            if gdf_type == 'Point':
                gdf_point = gdf.geometry.values[0]
                folium.CircleMarker(
                    location=(gdf_point.y, gdf_point.x),
                    radius=5,
                    color="#dbc72c",
                    fill=True,
                    fill_color="#dbc72c"
                ).add_to(mapObj)

            elif gdf_type == 'Polygon':
                sim_geo = gpd.GeoSeries(gdf.geometry.values[0]).simplify(tolerance=0.001)
                geo_j = sim_geo.to_json()
                geo_j = folium.GeoJson(data=geo_j, style_function=lambda x: {"fillColor": "#dbc72c"})
                geo_j.add_to(mapObj)

    return mapObj
