import pickle
import osmnx as ox


class Map():
    def __init__(self, mapObj, gdfs, map_point, all_tags, choosed_tags=None):
        self.mapObj = mapObj
        self.gdfs = gdfs
        self.map_point = map_point
        self.G_walk = ox.graph_from_point(map_point, network_type='walk')
        self.all_tags = all_tags
        self.choosed_tags = choosed_tags

class Persistence_Exemplar:
    """class for serialization/deserialization"""

    @staticmethod
    def serialize(account):
        with open('Map.pickle', 'wb') as f:
            pickle.dump(account, f)
        f.close()

    @staticmethod
    def deserialize():
        with open('Map.pickle', 'rb') as f:
            account = pickle.load(f)
        f.close()
        return account