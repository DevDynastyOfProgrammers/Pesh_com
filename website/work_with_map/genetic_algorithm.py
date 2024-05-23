from website.work_with_map.objects import Persistence_Exemplar

def create_priority():
    """
    пока временная(?) функция для добавления приоритета объекта
    """
    main_data = Persistence_Exemplar.deserialize()
    gdfs = main_data.gdfs
    gdfs = gdfs.assign(priority=3)
    gdfs.loc[gdfs['type']=='theatre', 'priority'] = 7
    print(type(gdfs), gdfs)