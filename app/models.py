from datetime import datetime
from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login
from hashlib import md5
from time import time
import jwt
from flask import current_app
from sqlalchemy.ext.declarative import declarative_base
from flask_migrate import migrate, upgrade
from flask import render_template, flash, redirect, url_for, request, g, current_app, json

Base = declarative_base()


followers = db.Table('followers',
    db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('followed_id', db.Integer, db.ForeignKey('user.id'))
)


cats = db.Table('cats',
    db.Column('tags_id', db.Integer, db.ForeignKey('tags.id')),
    db.Column('task_id', db.Integer, db.ForeignKey('task.id'))
)










class User(UserMixin,db.Model):
    
    id = db.Column(db.Integer, primary_key=True) 
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    firstname=db.Column(db.String(140))
    surname=db.Column(db.String(140))
    telefon=db.Column(db.String(140))
    mobile=db.Column(db.String(140))
    password_hash = db.Column(db.String(128))
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    tasks = db.relationship('Task', foreign_keys="[Task.created_by]", backref='author', lazy='dynamic')
    tasks_taken = db.relationship('Task', foreign_keys="[Task.taken_by]", backref='user', lazy='dynamic')
    mappoints = db.relationship('Mappoint',  backref='location', lazy='dynamic')
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    role=db.Column(db.String(24))
    create_date=db.Column(db.DateTime, index=True, default=datetime.utcnow)
    rating=db.Column(db.Integer)
    

    

    


    @login.user_loader
    #db relationship between left sider User(Parent Class) and right side user defined under ('User,...
    #secondary configures the association table I defined above the class
    #primaryjoin indicates thecondition that links the left side entity(the follower user) with the association table
    #secondaryjoin indicates the condition that links the right side user/the followed user) with the association table
    #backref defines how the the relationship will be acced from the right side user
        

    def load_user(id):
        return User.query.get(int(id))
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


    def __repr__(self):
        return '<User {}>'.format(self.username)

#Password reset token fields 

    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            current_app.config['SECRET_KEY'], algorithm='HS256').decode('utf-8')

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, current_app.config['SECRET_KEY'],
                            algorithms=['HS256'])['reset_password']
        except:
            return
        return User.query.get(id)

    followed = db.relationship(
        'User', secondary=followers,
        primaryjoin=(followers.c.follower_id == id),
        secondaryjoin=(followers.c.followed_id == id),
        backref=db.backref('followers', lazy='dynamic'), lazy='dynamic')

#functions to  follow unfollow user 

    def follow(self, user):
        if not self.is_following(user):
            self.followed.append(user)

    def unfollow(self, user):
        if self.is_following(user):
            self.followed.remove(user)

    def is_following(self, user):
        return self.followed.filter(
            followers.c.followed_id == user.id).count() > 0
#query all entries user followed



    def followed_posts(self):
        followed = Post.query.join(
            followers, (followers.c.followed_id == Post.user_id)).filter(
                followers.c.follower_id == self.id)
        own = Post.query.filter_by(user_id=self.id)
        return followed.union(own).order_by(Post.timestamp.desc())

#Create Avatar Icon for User

    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(
            digest, size)    



class Post(db.Model): # ,SearchableMixin needs to be added
    __searchable__ = ['body']
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    language = db.Column(db.String(5))
    def __repr__(self):
        return '<Post {}>'.format(self.body)


class Tags(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(64), unique=True)



class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    summary=db.Column(db.String(140))
    body = db.Column(db.String(1200))
    internet=db.Column(db.Boolean())
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    created_by= db.Column(db.Integer, db.ForeignKey('user.id'))
    taken_by= db.Column(db.Integer, db.ForeignKey('user.id'))
    tags = db.relationship('Tags', secondary='cats',backref='tasks')
    images = db.relationship('Images',backref='tasks_img')
    city_id = db.Column(db.Integer, db.ForeignKey('city.id'))
    price=db.Column(db.Float())
    currency=db.Column(db.String(32))
    status=db.Column(db.String(140))


class Images(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    path=db.Column(db.String(280))
    task_id = db.Column(db.Integer, db.ForeignKey('task.id'))


    





    def __repr__(self):
        return '<Post {}>'.format(self.body)


   


class Mappoint(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    streetname=db.Column(db.String(140))
    cityname=db.Column(db.String(64), unique=True)
    land=db.Column(db.String(64))
    number=db.Column(db.String(32))
    plz=db.Column(db.String(16), unique=True)
    additional_infos=db.Column(db.String(140))

class City(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(64), unique=True)
    citytasks = db.relationship('Task', backref='city', lazy='dynamic')


    




