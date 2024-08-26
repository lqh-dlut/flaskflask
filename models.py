from exts import db, db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
import datetime


class User(db.Model, UserMixin):
    # __bind_key__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False, default="default")
    #昵称
    username = db.Column(db.String(20), unique=True, nullable=False)
    #账户名（登录用）
    password_hash = db.Column(db.String(128), nullable=False) #此处存放密码哈希值
    email = db.Column(db.String(100), unique=True, nullable=True)
    jointime = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now)
    watchlist =db.relationship("Watchlist", backref="user", lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def validate_password(self, password):
        return check_password_hash(self.password_hash, password)

class Email_codetmp(db.Model):
    # __bind_key__ = "user"
    __tablename__ = 'email_codetmp'
    id = db.Column(db.Integer, primary_key=True)
    codetmp = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    reset_flag = db.Column(db.Boolean, nullable=False, default=False)

class Watchlist(db.Model):
    # __bind_key__ = "content"
    __tablename__ = 'watchlist'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(20))
    year = db.Column(db.String(4))
    filmnote = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    private_flag = db.Column(db.Boolean, nullable=False, default=True)

class HotMovie(db.Model):
    __tablename__ = 'hotmovie'
    # __bind_key__ = 'content'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(20))
    year = db.Column(db.String(4))
    rate = db.Column(db.String(4))
    url = db.Column(db.String(200))
