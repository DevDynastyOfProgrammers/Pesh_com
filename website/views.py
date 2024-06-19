from flask import Blueprint, render_template, request, flash, session, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from website.func import *
from website.work_with_map.create_a_route import *
from website.work_with_map.meta_data import Persistence_Exemplar
from website.UserLogin import UserLogin
from website import login_manager
from website.decorators import auth_role
import requests
import socket


def get_local_ip():
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
    return local_ip

views = Blueprint('views', __name__)

# Временные данные для удобства
default_speed = 1.1 * 60    # метров в минуту
walk_duration = 30
start_point = [64.54307276785013, 40.51783561706544]
end_point = [64.53672646553242, 40.531611442565925]
optimal_distance = default_speed*walk_duration//3

# test_map_html = 'test_map_html.html'

def render_map(mapObj):
    mapObj.get_root().render()
    header = mapObj.get_root().header.render()
    body_html = mapObj.get_root().html.render()
    script = mapObj.get_root().script.render()
    return header, body_html, script

@login_manager.user_loader
def load_user(user_id):
    return UserLogin().fromDB(user_id)

@views.route('/', methods=['GET'])
def mainWindow():
    
    logged = False
    if current_user.is_authenticated:
        logged = True

    show_all_features()
    
    # рендеринг карты
    mapObj = Persistence_Exemplar.deserialize().mapObj
    header, body_html, script = render_map(mapObj)
    window_map = render_template('map.html', header=header, 
                            body_html=body_html, script=script, logged=logged)

    return window_map

@views.route('/', methods=['POST'])
def user_route():

    logged = False
    if current_user.is_authenticated:
        logged = True

    points = [request.form[point].split() for point in request.form]

    # checking to correct coords
    for point in points:
        try:
            if not all(isinstance(float(coord), float) for coord in point):
                print('HUH!?')
                return mainWindow()
        except ValueError:
            print('not float')
            return mainWindow()
        if len(point) != 2:
            print('<2')
            return mainWindow()
        fpoint = [float(num) for num in point]
        points[points.index(point)] = fpoint
    
    mapObj = init_map(points[0])

    mapObj = show_all_features(mapObj=mapObj)

    for i in range(0, len(points)-1):
        first_point = points[i]
        second_point = points[i+1]
        mapObj = new_route(first_point, second_point, mapObj=mapObj)

    # рендеринг карты
    # mapObj = Persistence_Exemplar.deserialize().mapObj
    header, body_html, script = render_map(mapObj)
    window_map = render_template('map.html', header=header, 
                            body_html=body_html, script=script, logged=logged)

    return window_map

@views.route("/map_object/<object_name>", methods=["GET", "POST"])
def map_object(object_name):
    logged = False
    if current_user.is_authenticated:
        logged = True

    return render_template("map_object_info.html", object_name=object_name, 
                            logged=logged, is_not_profile=True)

@views.route("/login", methods=["POST", "GET"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('views.profile'))
    
    if request.method == "POST":
        user = get_user_by_email(request.form['email'])
        if user and check_password_hash(user.psw, request.form['psw']):
            userlogin = UserLogin().create(user)
            rm = True if request.form.get('remainme') else False
            login_user(userlogin, remember=rm)
            return redirect(request.args.get("next") or url_for("views.profile"))

        flash("Неверная пара логин/пароль", "error")
    return render_template("login.html", title="Авторизация")

@views.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('views.profile'))
    if request.method == "POST":
        # session.pop('_flashes', None)
        if len(request.form['name']) > 4 and len(request.form['email']) > 4 \
            and len(request.form['psw']) > 4 and request.form['psw'] == request.form['psw2']:
            hash = generate_password_hash(request.form['psw'])
            res = create_user(request.form['name'], request.form['email'], hash)

            if res:
                add_role_to_user(res, request.form['select'])
                flash("Вы успешно зарегистрированы", "success")
                return redirect(url_for('views.login'))
            else:
                flash("Ошибка при добавлении в БД", "error")
        else:
            flash("Неверно заполнены поля", "error")
    return render_template("register.html", title="Регистрация")

@views.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Вы вышли из аккаунта", "success")
    return redirect(url_for('views.login'))

@views.route("/dir")
def event():
    logged = False
    if current_user.is_authenticated:
        logged = True

    is_admin = False
    try:
        if current_user.has_role('admin') != None:
            is_admin = True
    except AttributeError: 
        print('зашел незарегестрированный пользователь')
    events = read_events()
    return render_template("spravochnik.html", events=events, 
                            logged=logged, is_admin=is_admin, 
                            is_not_profile=True)


@views.route("/xu", methods=["GET"])
# @login_required   # необходимость авторизации 
# @auth_role(['admin'])     # нужна роль админа
def event_info():
    logged = False
    if current_user.is_authenticated:
        logged = True

    event_id = request.args.get("id")
    event = get_event_by_id(event_id)
    place = event.place

    # real_ip = request.headers.get('X-Real-IP', request.remote_addr)
    # print(real_ip)

    # if request.headers.get('X-Forwarded-For'):
    #     ip = request.headers['X-Forwarded-For']
    # else:
    #     ip = request.remote_addr

    # url = f"http://ipinfo.io/{ip}/geo"
    # response = requests.get(url)
    # data = response.json()
    # ip_addr = request.environ['REMOTE_ADDR']
    # print(data, ip, ip_addr, get_local_ip())
    # latitude = data['loc'].split(',')[0]
    # longitude = data['loc'].split(',')[1]
    # print(longitude, latitude)

    start_point = [64.54209318126482, 40.53486109285977]
    end_point = [place.longitude, place.latitude]
    
    mapObj = init_map(start_point, width=1000, height=520)
    if place.longitude != None and place.latitude != None:
        new_route(start_point, end_point, mapObj=mapObj)
    
    custom_marker = folium.CircleMarker(
        location=end_point,
        radius=5,
        color="#dbc72c",
        fill=True,
        fill_color="#dbc72c"
    ).add_to(mapObj)

    mapObj.get_root().width = "1000px"
    mapObj.get_root().height = "600px"
    iframe = mapObj.get_root()._repr_html_()
    
    return render_template("info.html", event=event, 
                            place=place, logged=logged, 
                            iframe=iframe, is_not_profile=True)

@views.route('/profile', methods=["POST", "GET"])
@login_required
def profile():
    routes = (Route
                .select()
                .join(UserRoute)
                .join(User)
                .where(User.name == current_user.get_name()))
    
    return render_template("profile.html", 
                            current_user=current_user, routes=routes,
                            is_not_profile=False)

@views.route('/route', methods=["POST", "GET"])
@login_required
def route_detail():
    route_id = request.args.get("id")

    route = Route.get_or_none(Route.route_id == route_id)

    connections = (Connection
                    .select()
                    .join(RouteConnection)
                    .join(Route)
                    .where(Route.name == route.name))
    
    mapObj = init_map([64.54307276785013, 40.51783561706544], width=1000, height=520) #! заменить на нормальную точку
    for connection in connections:
        start_point = [connection.start_point.longitude, connection.start_point.latitude]
        end_point = [connection.end_point.longitude, connection.end_point.latitude]
        mapObj = new_route(start_point, end_point, mapObj=mapObj)

        mapObj.get_root().width = "1000px"
        mapObj.get_root().height = "600px"
        iframe = mapObj.get_root()._repr_html_()
    
    return render_template("route.html", 
                            current_user=current_user, route=route,
                            connections=connections, iframe=iframe,
                            is_not_profile=True)
