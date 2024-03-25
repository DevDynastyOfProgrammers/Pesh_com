import osmnx as ox

ox.config(log_console=True, use_cache=True)

G_walk = ox.graph_from_place('Manhattan Island, New York City, New York, USA',
                            network_type='walk')