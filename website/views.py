from flask import Blueprint, render_template, request, flash, session, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required
from website.func import *
from website.work_with_map.create_a_route import *
from website.work_with_map.meta_data import Persistence_Exemplar
from website.UserLogin import UserLogin
from website import login_manager


views = Blueprint('views', __name__)

# Временные данные для удобства
default_speed = 1.1 * 60    # метров в минуту
walk_duration = 30
start_point = [64.54307276785013, 40.51783561706544]
end_point = [64.53672646553242, 40.531611442565925]

# test_map_html = 'test_map_html.html'

@login_manager.user_loader
def load_user(user_id):
    print("load_user")
    return UserLogin().fromDB(user_id)

@views.route('/', methods=['GET', 'POST'])
def mainWindow():
    
    # добавление маршрута на карту
    new_route(start_point, end_point)

    # вывод точек интереса
    # show_selected_features(tags=None)
    # show_features()
    show_all_features()

    # вывод области прогулки
    optimal_distance = default_speed*walk_duration//3

    show_walking_area(start_point, optimal_distance)
    near_features(start_point, optimal_distance)

    # select_features_for_walk(start_point, optimal_distance, tags=None)
    
    # рендеринг карты
    mapObj = Persistence_Exemplar.deserialize().mapObj
    mapObj.get_root().render()
    header = mapObj.get_root().header.render()
    body_html = mapObj.get_root().html.render()
    script = mapObj.get_root().script.render()
    window_map = render_template('home.html', header=header, 
                            body_html=body_html, script=script)

    # сохраняем html как файл, чтобы просмотреть весь код страницы
    # mapObj.save(test_map_html)
    # with open(test_map_html, 'w') as mapfile:
    #     mapfile.write(window_map)

    return window_map

@views.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        user = get_user_by_email(request.form['email'])
        print(user.psw, request.form['psw'])
        if user and check_password_hash(user.psw, request.form['psw']):
            userlogin = UserLogin().create(user)
            login_user(userlogin)
            return redirect(url_for('views.mainWindow'))

        flash("Неверная пара логин/пароль", "error")
    return render_template("login.html", title="Авторизация")

@views.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == "POST":
        # session.pop('_flashes', None)
        if len(request.form['name']) > 4 and len(request.form['email']) > 4 \
            and len(request.form['psw']) > 4 and request.form['psw'] == request.form['psw2']:
            hash = generate_password_hash(request.form['psw'])
            res = create_user(request.form['name'], request.form['email'], hash)
            if res:
                flash("Вы успешно зарегистрированы", "success")
                return redirect(url_for('views.login'))
            else:
                flash("Ошибка при добавлении в БД", "error")
        else:
            flash("Неверно заполнены поля", "error")
    return render_template("register.html", title="Регистрация")

@views.route("/dir")
def event():
    events = read_events()
    return render_template("spravochnik.html", events=events)


@views.route("/xu", methods=["GET"])
# @login_required
def event_info():
    event_id = request.args.get("id")
    event = get_event_by_id(event_id)
    place = event.place
    return render_template("info.html", event=event, place=place)
