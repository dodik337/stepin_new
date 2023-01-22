# taskkill /f /im python.exe
#
import datetime
import os
import sqlite3
import time
import math
from flask import Flask, render_template, flash, redirect, session, url_for, request, abort, g
import git

from fdatabase import FDataBase
from forms import LoginForm

from config import Config

app = Flask(__name__)
app.config.from_object(Config)
app.config.update(dict(DATABASE=os.path.join(app.root_path, 'fdb.db')))
app.permanent_session_lifetime = datetime.timedelta(seconds=60)


def connect_db():
    conn = sqlite3.connect(app.config['DATABASE'])
    conn.row_factory = sqlite3.Row
    return conn
def get_db():
    if not  hasattr(g, 'link_db'):
        g.link_db = connect_db()
        return g.link_db

@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'link_db'):
        g.link_db.close()

@app.route('/update_server', methods=['POST', 'GET'])
def webhook():
    if request.method == 'POST':
        repo = git.Repo('/home/mypythonprojects/stepin_new')
        origin = repo.remotes.origin
        origin.pull()
        return 'Сайт обновился', 200
    else:
        return 'Возникла ошибка', 400

@app.route('/kuku')
def hi():  # put application's code here
    return 'sdfsdf!'

@app.route('/aaaaa')
def aaaaa():  # put application's code here
    return 'ssssssssssssssss'

@app.route('/post', methods=['POST', 'GET'])
def post():
    db = get_db()
    database = FDataBase(db)
    tm = math.floor(time.time())
    if request.method == "POST":
        if len(request.form['name']) > 3 and len(request.form['post']) > 10:
            res = database.addPost(request.form['name'], request.form['post'])
            if not res:
                flash('Ошибка добавления статьи', category='error')
            else:
                flash('Статья добавлена успешно', category='success')
        else:
            flash('Ошибка добавления статьи', category='error')

    return render_template('posts.html', title='Пост', menu=database.getMenu())


@app.route('/login', methods=['GET', 'POST'])
def login():  # put application's code here
    form = LoginForm()
    print(form.validate_on_submit())
    if form.validate_on_submit():
        flash(f"Зашел пользователь под логином {form.username.data}, запомнить = {form.remember_me.data}")
        return redirect('/index')

    return render_template('login.html', title='Авторизация пользователя', form=form)


users_passwords = {'1': '12', 'user2': 'password2', 'user3': 'password3',
                   'user4': 'password4', 'user5': 'password5', 'user6': 'password6', 'user7': 'password7',
                   'user8': 'password8'}


@app.route('/login2', methods=['POST', 'GET'])
def login2():
    if 'userlogged' in session:
        return redirect(url_for('profile', username=session['userlogged']))
    elif request.method == 'POST' and request.form['username'] in users_passwords \
            and request.form['psw'] == users_passwords[request.form['username']]:
        session['userlogged'] = request.form['username']
        return redirect(url_for('profile', username=session['userlogged']))

    return render_template('login_2var.html', title='Авторизация пользователя')


@app.route('/profile/<username>')
def profile(username):
    if 'userlogged' not in session or session['userlogged'] != username:
        abort(401)
    return f"<h1> Пользователь {username}"


@app.route('/')
@app.route('/index')
def index():  # put application's code here
    db = get_db()
    database = FDataBase(db)


    car = {'name': ('bugatty',

                    'https://libertycity.ru/uploads/download/gta5_bugatti/fulls/j4q9k776k31rt5p2jnd2823s63/15043684584016_f61541-1.jpg')}

    return render_template('index.html', name=car['name'][0], foto=car['name'][1], title='1', menu=database.getMenu())


@app.route('/petya/')
def petya():  # put application's code here
    return ''' <h2> Александр Твардовский

Василий Теркин. Сборник

Лирика

РОДНОЕ

<br>Дорог израненные спины, </br>
<br>О дальних шумных городах. </br>
    </h2> '''


# @app.route('/user/<username>')
# def user_profile(username):  # put application's code here
#     return f"<h1>Здраствуй дорогой пользователь {username}</h1>"
#
#
# @app.route('/user/<int:post_id>')
# def show_post(post_id):  # put application's code here
#     return f"<h1>Горячая и свежая новость № {post_id}</h1>"


@app.errorhandler(404)
def page_not_found(error):
    return render_template('page404.html', title='Страница не найдена')


if __name__ == '__main__':
    app.run(debug=True)
