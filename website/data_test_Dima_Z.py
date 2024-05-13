import folium
import requests

# Инициализируем карту
map = folium.Map(location=[64.5431, 40.5378], zoom_start=13) # Начальные координаты и масштаб

# Добавляем слой карты OpenStreetMap с атрибуцией по умолчанию
folium.TileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', attr='OpenStreetMap').add_to(map)

# Функция для получения мероприятий из API OpenTripMap
def get_events(api_key, latitude, longitude, radius):
    url = f"https://api.opentripmap.com/0.1/en/places/radius?radius={radius}&lon={longitude}&lat={latitude}&apikey={api_key}"
    response = requests.get(url)
    data = response.json()
    print(data)
    return data['features']

# Пример использования
api_key = '5ae2e3f221c38a28845f05b6d998922a5fc30f62ce922890ec391fe8'
latitude = 64.5431
longitude = 40.5378
radius = 100000 # В метрах

events = get_events(api_key, latitude, longitude, radius)
for event in events:
    geometry = event['geometry']
    properties = event['properties']
    name = properties['name']
    coordinates = geometry['coordinates']

    # Создание маркера для каждого мероприятия и добавление его на карту
    folium.Marker(location=[coordinates[1], coordinates[0]], popup=name).add_to(map)
    break

# Сохраняем карту в файл
map.save('map.html')