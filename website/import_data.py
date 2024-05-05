import osmnx as ox
import numpy as np
import pandas as pd


def osm_query(tag, city):
    gdf = ox.geometries_from_place(city, tag).reset_index()
    gdf['city'] = np.full(len(gdf), city.split(',')[0])
    gdf['object'] = np.full(len(gdf), list(tag.keys())[0])
    gdf['type'] = np.full(len(gdf), tag[list(tag.keys())[0]])
    gdf = gdf[['city', 'object', 'type', 'geometry']]
    print(gdf.shape)
    return gdf

def get_lat_lon(geometry):
        
    lon = geometry.apply(lambda x: x.x if x.type == 'Point' else x.centroid.x)
    lat = geometry.apply(lambda x: x.y if x.type == 'Point' else x.centroid.y)
    return lat, lon

# Выгрузим интересующие нас категории объектов 
tags = [
    {'building' : True }
]
cities = ['Архангельск, Россия']

gdfs = []
for city in cities:
    for tag in tags:
        gdfs.append(osm_query(tag, city))
        
# посмотрим что получилось
data_poi = pd.concat(gdfs)
data_poi.groupby(['city','object','type'], as_index = False).agg({'geometry':'count'})

# добавим координаты/центроиды
lat, lon = get_lat_lon(data_poi['geometry'])
data_poi['lat'] = lat
data_poi['lon'] = lon

print(data_poi)