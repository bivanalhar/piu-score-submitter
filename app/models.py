from datetime import datetime
from app import db
from app import login
from hashlib import md5

from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(64), index = True, unique = True)
    email = db.Column(db.String(128), index = True, unique = True)
    password_hash = db.Column(db.String(128))
    about_me = db.Column(db.String(200))
    last_seen = db.Column(db.DateTime, default = datetime.utcnow)
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    scores = db.relationship('Score', backref='author', lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(digest, size)

class Score(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(64))
    perfect = db.Column(db.Integer, default = 0)
    great = db.Column(db.Integer, default = 0)
    good = db.Column(db.Integer, default = 0)
    bad = db.Column(db.Integer, default = 0)
    miss = db.Column(db.Integer, default = 0)
    totalScore = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Perfect:{} Great:{} Good:{} Bad:{} Miss:{}>'.format(self.perfect, self.great, \
            self.good, self.bad, self.miss)
    
    def set_totalScore(self, perfect, great, good, bad, miss):
        self.totalScore = 2 * perfect + 1 * great + 0 * (good + bad + miss)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    body = db.Column(db.String(128))
    timestamp = db.Column(db.DateTime, index = True, default = datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Post {}>'.format(self.body)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))