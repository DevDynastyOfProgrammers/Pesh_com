from peewee import *
import datetime
import pickle
# from meta_data import Persistence_Exemplar
import pandas as pd
import numpy as np
import osmnx as ox
import pandas as pd
import geopandas as gpd


map_point = [64.53821631881615, 40.513887405395515]
all_tags = [
    {'amenity' : 'theatre' },
    {'historic' : True}
]

db = PostgresqlDatabase('neondb', host='ep-bitter-wind-a2twehp1.eu-central-1.aws.neon.tech', port=5432,
                        user='neondb_owner', password='9kuNsG0jbvhe')


class BaseModel(Model):
    class Meta:
        database = db

class Place(BaseModel):
    place_id = AutoField()
    name = TextField(null=False, unique=True)
    description = TextField()
    longitude = DoubleField()
    latitude = DoubleField()
    # gdf = AnyField()
    class Meta:
        table_name = 'place'

def _osm_query(all_tags, map_point):
    """
    Импорт данных объекта/-ов из OSM по 1 тегу.
    """
    gdf = ox.features_from_point(map_point, all_tags).reset_index()
    gdf['object'] = np.full(len(gdf), list(all_tags.keys())[0])
    gdf['type'] = np.full(len(gdf), all_tags[list(all_tags.keys())[0]])
    # print(gdf.__dict__)
    # print(gdf[['element_type', 'osmid', 'name', 'name:en', 'start_date', 'website', 'wikidata',
    #     'wikipedia', 'geometry', 'wheelchair', 'operator', 'opening_hours', 'alt_name',
    #     'phone', 'nodes', 'addr:housenumber', 'addr:street', 'building', 'building:levels', 'amenity','object', 'type']])
    # print(gdf[['osmid', 'name', 'start_date', 'website']])
    gdf = gdf[['osmid', 'name', 'object', 'type', 'geometry', 'start_date', 'website']]
    
    return gdf

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

def _get_point_coords(geometry: "gpd.geoseries.GeoSeries") -> 'tuple':
    """
    Получение координат точки (или центра точек) объекта Point и других
    Использует geopandas.geoseries.GeoSeries (на данный момент это gdf['geometry'])
    Вывод кортеж широты и долготы объекта. Если это полигон, то выводит центрированную точку
    """
    lon = geometry.apply(lambda x: x.x if x.geom_type == 'Point' else x.centroid.x)
    lat = geometry.apply(lambda x: x.y if x.geom_type == 'Point' else x.centroid.y)
    return lat.iloc[0], lon.iloc[0]

def create_place(name, place_id=AutoField(), description=''):
    """Создает новое место"""
    place = Place(place_id=place_id, name=name, description=description)
    place.save()
    return place


if __name__ == '__main__':
    gdfs = _get_featuters(map_point, all_tags)
    keys = gdfs.keys().to_list()
    # for gdf in gdfs.values:
    #     gdf_type= gdf[keys.index('geometry')]
    #     print(gdfs.iloc[[0]].geometry)

    #     print(gdf_type)
    #     if gdf_type not in ['Point', 'Polygon']:
    #         continue
    #     if gdf_type == 'Point':
    #         coords = gdf.geometry.values[0]
    #         location = (coords.y, coords.x)
    #     elif gdf_type == 'Polygon':
    #         # print()
    #         # print()
    #         # print(gdf['geometry'], type(gdf['geometry']))
    #         # print()
    #         # print()
    #         coords = _get_point_coords(gdf['geometry'])
    #         location = (coords[0], coords[1])
    #     print(location)
    #     break

    for index, gdf in gdfs.iterrows():
        # _get_point_coords(gdf['geometry'])
        print(gdf['geometry'])
        break
    # print(gdfs)