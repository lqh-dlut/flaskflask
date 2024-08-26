import os
import sys
import pymysql
import click
import config
import redis
from flask import Flask, request, redirect, flash
from flask import url_for
from flask import render_template
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from exts import db, init_extensions
from register_blueprints import register_blueprints
from models import User, Watchlist, HotMovie, Email_codetmp

app = Flask(__name__)
#绑定配置文件
app.config.from_object(config)
app.secret_key = 'dev'
pymysql.install_as_MySQLdb()

register_blueprints(app)

init_extensions(app)


@app.context_processor
def inject_user():  # 函数名可以随意修改
    user = User.query.first()
    return dict(user=user)  # 需要返回字典，等同于 return {'user': user}

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if not current_user.is_authenticated:
        # Todo: 判断是否是该用户的数据，是否是private，只有非private和个人数据才能显示在index中 DONE

            return redirect(url_for('index'))
        user_id = current_user.id
        title = request.form['title']
        year = request.form['year']
        #验证数据
        if not title or not year or len(year) != 4 or len(title) > 60:
            flash('Invalid title or year')
            return redirect(url_for('index')) #重定向回主页
        movie = Watchlist(title = title, year = year, user_id = user_id)
        db.session.add(movie)
        db.session.commit()
        flash("Item created successfully")
        return redirect(url_for('index'))


    #user = User.query.first() inject_user()将user函数嵌入，模板不需要再user
    movies = Watchlist.query.all()
    return render_template('index.html',movies=movies)

# @app.errorhandler(404)  # 传入要处理的错误代码
# def page_not_found(e):  # 接受异常对象作为参数
#     user = User.query.first()
#     return render_template('error.html', user=user), 404  # 返回模板和状态码

@app.errorhandler(Exception)  # 传入要处理的错误代码
def page_not_found(e):  # 接受异常对象作为参数
    user = User.query.first()
    return render_template('error.html', error=str(e))  # 返回模板和状态码

#命令
@app.cli.command()  # 注册为命令，可以传入 name 参数来自定义命令
@click.option('--drop', is_flag=True, help='Create after drop.')  # 设置选项
def initdb(drop):
    with app.app_context():
        if drop:
            db.drop_all()
        db.create_all()
        click.echo('Initialized the database.')

@click.option('--username', prompt=True, help='The username used to login')
@click.option('--password', prompt=True, hide_input=True, confirmation_prompt=True)
@app.cli.command()
def admin(username, password):
    db.create_all()
    user = User.query.first()

    if user is not None:
        click.echo('Updating Admin...')
        user.set_password(password)
        user.username = username
    else:
        click.echo('Creating Admin...')
        user = User(username = username, name='Admin')
        user.set_password(password)
        db.session.add(user)

    db.session.commit()
    click.echo('Done.')

@app.cli.command()
def forge():
    db.create_all()
    name = 'JJY'
    movies = [
    {'title': 'My Neighbor Totoro', 'year': '2222'  },
    {'title': 'Dead Poets Society', 'year': '1989'},
    {'title': 'A Perfect World', 'year': '1993'},
    {'title': 'Leon', 'year': '1994'},
    {'title': 'Mahjong', 'year': '1996'},
    {'title': 'Swallowtail Butterfly', 'year': '1996'},
    {'title': 'King of Comedy', 'year': '1999'},
    {'title': 'Devils on the Doorstep', 'year': '1999'},
    {'title': 'WALL-E', 'year': '2008'},
    {'title': 'The Pork of Music', 'year': '2012'},
]

    movies2 = [
        {'title': 'My', 'year': '1988'},
        {'title': 'Dead', 'year': '1989'},
        {'title': 'A', 'year': '1993'},
        {'title': 'Leon', 'year': '1994'},
        {'title': 'Mahjong', 'year': '1996'},
        {'title': 'Swallowtail', 'year': '1996'},
        {'title': 'King', 'year': '1999'},
        {'title': 'Devils', 'year': '1999'},
        {'title': 'WALL-E', 'year': '2008'},
        {'title': 'The', 'year': '2012'},
    ]
    user = User(name=name)
    db.session.add(user)
    # db2.session.add(user)
    for m in movies:
        movie = Watchlist(title = m['title'], year = m['year'])
        db.session.add(movie)
    for m in movies2:
        movie = HotMovie(title = m['title'], year=m['year'])
        db.session.add(movie)
    db.session.commit()
    click.echo('Done.')

#initialize Flask_login
login_manager = LoginManager(app)
login_manager.login_view = 'login'
@login_manager.user_loader
def load_user(user_id):
    user = User.query.get(int(user_id))
    return user

