import osmnx as ox
import numpy as np
import pandas as pd


def osm_query(tag, city):
    gdf = ox.features_from_point(map_point, tag).reset_index()
    gdf['object'] = np.full(len(gdf), list(tag.keys())[0])
    gdf['type'] = np.full(len(gdf), tag[list(tag.keys())[0]])
    gdf = gdf[['name', 'object', 'type', 'geometry']]
    
    return gdf

def get_lat_lon(geometry):
    lon = geometry.apply(lambda x: x.x if x.geom_type == 'Point' else x.centroid.x)
    lat = geometry.apply(lambda x: x.y if x.geom_type == 'Point' else x.centroid.y)
    return lat, lon

# Выгрузим интересующие нас категории объектов 
tags = [
    {'amenity' : 'theatre' }
]
map_point = [64.53821631881615, 40.513887405395515]

gdfs = []
for tag in tags:
    gdfs.append(osm_query(tag, map_point))
        
# посмотрим что получилось
data_poi = pd.concat(gdfs)
data_poi.groupby(['name','object','type'], as_index = False).agg({'geometry':'count'})

# добавим координаты/центроиды
lat, lon = get_lat_lon(data_poi['geometry'])
data_poi['lat'] = lat
data_poi['lon'] = lon

print(type(gdfs[0]))
print(data_poi)
