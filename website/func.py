from website.baza import *


def get_event_by_id(event_id):
    """Возвращает данные мероприятия по его ID"""
    return Event.get_or_none(Event.event_id == event_id)

def get_user_by_id(user_id):
    return User.get_or_none(User.user_id == user_id)

def get_user_by_email(email):
    return User.get_or_none(User.email == email)

# def user_has_role(user_id):
#     return User.get_or_none(User.user_id == UserRole.user_id)

def create_place(name, description):
    """Создает новое место"""
    place = Place(name=name, description=description)
    place.save()
    return place

def create_user(name, email, psw):
    """Регистрируем пользователя в системе"""
    if User.get_or_none(User.email == email) or User.get_or_none(User.name == name):
        return False
    user = User(name=name, email=email, psw=psw)
    user.save()
    return user

def create_event(name, start_date, end_date, place, price, start_time, type):
    """Создает новое событие"""
    event = Event(name=name, start_date=start_date, end_date=end_date, place=place, price=price, start_time=start_time, type=type)
    event.save()
    return event

def read_places():
    """Возвращает список всех мест"""
    return Place.select()

def read_events():
    """Возвращает список всех событий"""
    return Event.select()

def read_users():
    """Возвращает список всех пользователей"""
    return User.select()

def read_place_by_id(place_id):
    """Возвращает место по ID"""
    return Place.get_or_none(Place.place_id == place_id)


def read_event_by_id(event_id):
    """Возвращает событие по ID"""
    return Event.get_or_none(Event.event_id == event_id)


def update_place(place_id, name, description):
    """Обновляет место"""
    place = read_place_by_id(place_id)
    if place:
        place.name = name
        place.description = description
        place.save()
        return place
    return None


def update_event(event_id, name, start_date, end_date, place, price, start_time, type):
    """Обновляет событие"""
    event = read_event_by_id(event_id)
    if event:
        event.name = name
        event.start_date = start_date
        event.end_date = end_date
        event.place = place
        event.price = price
        event.start_time = start_time
        event.type = type
        event.save()
        return event
    return None


def delete_place(place_id):
    """Удаляет место"""
    place = read_place_by_id(place_id)
    if place:
        place.delete_instance()
        return True
    return False


def delete_event(event_id):
    """Удаляет событие"""
    event = read_event_by_id(event_id)
    if event:
        event.delete_instance()
        return True
    return False
