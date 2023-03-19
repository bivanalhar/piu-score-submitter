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
    title = db.Column(db.Integer)
    last_seen = db.Column(db.DateTime, default = datetime.utcnow)
    scores = db.relationship('Score', backref='author', lazy='dynamic')

    def __repr__(self):
        return '<User {}, Title {}>'.format(self.username, self.title)

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
    event = db.Column(db.String(200))
    chart = db.Column(db.String(200))
    perfect = db.Column(db.Integer, default = 0)
    great = db.Column(db.Integer, default = 0)
    good = db.Column(db.Integer, default = 0)
    bad = db.Column(db.Integer, default = 0)
    miss = db.Column(db.Integer, default = 0)
    finalScore = db.Column(db.Float)
    setNumber = db.Column(db.Integer, default = 1)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<ID:{} Username:{} Event:{} Chart:{} finalScore:{} setNumber:{}>'.format(self.id, self.username, self.event, self.chart, self.finalScore, self.setNumber)

    def set_totalScore(self, perfect, great, good, bad, miss):
        numerator = perfect + 0.8*great + 0.5*good + 0.1*bad
        denominator = perfect + great + good + bad + miss
        self.finalScore = int(numerator * 10000000 / denominator) / 100000

class Chart(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    event = db.Column(db.String(128))
    chart = db.Column(db.String(200))

    def __repr__(self):
        return '<ID:{} Chart:{} Event:{}>'.format(self.id, self.chart, self.event)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))