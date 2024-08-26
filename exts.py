#flask-sqlalchemy
import pymysql
import redis
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from celery import Celery

db = SQLAlchemy()
pool = redis.ConnectionPool(host='localhost', port=6379, db=0)
redis_client = redis.Redis(connection_pool=pool)
mail = Mail()
celery = Celery('hotmovie')


def init_extensions(app):
    db.init_app(app)
    mail.init_app(app)
    celery.conf.update(app.config)


