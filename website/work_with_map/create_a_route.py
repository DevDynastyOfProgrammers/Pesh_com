import folium
import numpy as np
import osmnx as ox
import networkx as nx
import pandas as pd
import geopandas as gpd
import math
from website.work_with_map.meta_data import Persistence_Exemplar

# Вспомогательные функции

def init_map(map_point, width=2000, height=1000):
    mapObj = folium.Map(location=map_point, tiles="cartodbpositron", zoom_start=15, width=width, height=height)
    return mapObj

def init_map_data(map_point, all_tags):
    #! НЕ ТРОГАТЬ, НЕ ИСПОЛЬЗОВАТЬ
    """вызывается один раз в __init__.py"""
    mapObj = init_map(map_point)
    gdfs = _get_featuters(map_point, all_tags)
    return mapObj, gdfs

def _osmid_to_coords(graph, ids):
    """
    Вывод координат объекта по его ID в OSM
    """
    coords = []
    for i in range(1, len(ids)):
        coords.append([graph.nodes[ids[i]]['y'], graph.nodes[ids[i]]['x']])
    return coords

def _osm_query(all_tags, map_point):
    """
    Импорт данных объекта/-ов из OSM по 1 тегу.
    """
    gdf = ox.features_from_point(map_point, all_tags).reset_index()
    gdf['object'] = np.full(len(gdf), list(all_tags.keys())[0])
    gdf['type'] = np.full(len(gdf), all_tags[list(all_tags.keys())[0]])
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

def get_meta_data(func):
    def get_data(*args,**rwargs):
        main_data = Persistence_Exemplar.deserialize()
        mapObj = main_data.mapObj

        func(mapObj=mapObj, *args,**rwargs)

        main_data.mapObj = mapObj
        Persistence_Exemplar.serialize(main_data)
    return get_data

# Основные функции
def new_route(start_point, end_point, mapObj=None):
    """
    добавляет на карту (mapObj) маршрут по координатам начального и конечного места
    СДЕЛАТЬ ДЕКОРАТОР
    """

    main_data = Persistence_Exemplar.deserialize()
    is_meta = False
    if mapObj == None:
        mapObj = main_data.mapObj
        is_meta = True

    ox.config(log_console=True, use_cache=True)

    G_walk = main_data.G_walk

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

    if is_meta == True:
        main_data.mapObj = mapObj
        Persistence_Exemplar.serialize(main_data)
    return mapObj

def _get_custom_gdfs(tags=None):
    main_data = Persistence_Exemplar.deserialize()
    map_point = main_data.map_point

    if tags != None:
        gdfs = _get_featuters(map_point, tags)
    else:
        gdfs = main_data.gdfs
    custom_gdfs = []

    for gdf_id in range(len(gdfs.values)):
        gdf = gdfs.iloc[[gdf_id]]
        custom_gdfs.append(gdf)
    return custom_gdfs

def _show_feature(mapObj, gdf, gdf_type, color):
    if gdf_type not in ['Point', 'Polygon']:
        return False
    if gdf_type == 'Point':
        coords = gdf.geometry.values[0]
        location = (coords.y, coords.x)
    elif gdf_type == 'Polygon':
        coords = _get_point_coords(gdf['geometry'])
        location = (coords[0], coords[1])
        
    folium.CircleMarker(
        location=location,
        radius=5,
        color=color,
        fill=True,
        fill_color=color
    ).add_to(mapObj)
    #? Почему-то, если сохрять данные в виде полигонов, то говорит, что данные локальные и их нельзя сериализовать
    # elif gdf_type == 'Polygon':
    #     sim_geo = gpd.GeoSeries(gdf.geometry.values[0]).simplify(tolerance=0.001)
    #     geo_j = sim_geo.to_json()
    #     geo_j = folium.GeoJson(data=geo_j, style_function=lambda x: {"fillColor": "pink"})
    #     geo_j.add_to(mapObj)
    
    return mapObj

def show_features(func):
    def check(*args, **kwargs):
        main_data = Persistence_Exemplar.deserialize()
        mapObj = main_data.mapObj
        tags = main_data.choosed_tags

        custom_gdfs = _get_custom_gdfs(tags)

        for gdf in custom_gdfs:
            gdf_type = gdf.geom_type.values[0]

            res, color = func(gdf, *args, **kwargs)
            if not res:
                continue

            features = _show_feature(mapObj, gdf, gdf_type, color=color)
            if not features:
                continue
            else:
                mapObj = features
        
        main_data.mapObj = mapObj
        Persistence_Exemplar.serialize(main_data)
        return mapObj
    
    return check

@show_features
def near_features(gdf, center, radius):
    coords = _get_point_coords(gdf['geometry'])
    distance = _points_dist(coords[0], coords[1], center[0], center[1])
    color = "#dbc72c"
    return distance < radius, color

@show_features
def show_all_features(gdf):
    color="#df8143"
    return True, color

def show_walking_area(start_point, optimal_distance, mapObj=None):
    main_data = Persistence_Exemplar.deserialize()
    mapObj = main_data.mapObj

    folium.Circle(
        location=start_point,
        radius=optimal_distance,
        # color="black",
        weight=0,
        fill_opacity=0.4,
        opacity=1,
        fill_color="green",
        fill=False,  # gets overridden by fill_color
        # popup="{} meters".format(optimal_distance),
        # tooltip="I am in meters",
    ).add_to(mapObj)

    main_data.mapObj = mapObj
    Persistence_Exemplar.serialize(main_data)
    return mapObj
