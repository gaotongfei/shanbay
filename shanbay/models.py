from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from . import login_manager

user_word = db.Table('user_word', db.Model.metadata,
                     db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
                     db.Column('word_id', db.Integer, db.ForeignKey('word.id')))

user_word_known = db.Table('user_word_known', db.Model.metadata,
                           db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
                           db.Column('word_id', db.Integer, db.ForeignKey('word.id')))


class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False, index=True)
    email = db.Column(db.String(50), nullable=False, unique=True)
    password_hash = db.Column(db.String(128))
    new_user = db.Column(db.Integer, default=1)
    # backref 可加可不加
    words = db.relationship('Word', secondary=user_word,
                            backref=db.backref('users', lazy='dynamic'), lazy='dynamic')
    words_known = db.relationship('Word', secondary=user_word_known, lazy='dynamic')
    words_per_day = db.Column(db.Integer)
    category = db.Column(db.String(20))

    @property
    def password(self):
        raise AttributeError('Password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __init__(self, username, email):
        self.username = username
        self.email = email

    def __repr__(self):
        return "<User %r>" % self.username


class Word(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    word = db.Column(db.String(100), nullable=False)
    translation = db.Column(db.String(500))
    category = db.Column(db.String(20))

    def __init__(self, word, translation=None, category=None):
        self.word = word
        self.translation = translation
        self.category = category


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
