from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from . import login_manager
from datetime import datetime

user_word = db.Table('user_word', db.Model.metadata,
                     db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
                     db.Column('word_id', db.Integer, db.ForeignKey('word.id')))

user_word_known = db.Table('user_word_known', db.Model.metadata,
                           db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
                           db.Column('word_id', db.Integer, db.ForeignKey('word.id')))

'''
word_note = db.Table('word_note', db.Model.metadata,
                     db.Column('word_id', db.Integer, db.ForeignKey('word.id')),
                     db.Column('note_id', db.Integer, db.ForeignKey('note.id')))

user_note = db.Table('user_note', db.Model.metadata,
                     db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
                     db.Column('note_id', db.Integer, db.ForeignKey('note.id')))
'''


class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, index=True)
    email = db.Column(db.String(50), unique=True)
    password_hash = db.Column(db.String(128))
    new_user = db.Column(db.Integer, default=1)
    # backref 可加可不加
    words = db.relationship('Word', secondary=user_word,
                            backref='users', lazy='dynamic')
    words_known = db.relationship('Word', secondary=user_word_known, lazy='dynamic')
    notes = db.relationship('Note', backref='users', lazy='dynamic')
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

    def __init__(self, username=None, email=None, password=None):
        self.username = username
        self.email = email
        self.password = password

    def __repr__(self):
        return "<User %r>" % self.username


class Word(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    word = db.Column(db.String(100), nullable=False)
    translation = db.Column(db.String(500))
    category = db.Column(db.String(20))
    notes = db.relationship('Note', backref='words', lazy='dynamic')
    # attribute :users: backrefed by User

    def __init__(self, word, translation=None, category=None):
        self.word = word
        self.translation = translation
        self.category = category

    def __repr__(self):
        return "<Word %r>" % self.word


class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    created_time = db.Column(db.DateTime, default=datetime.utcnow())
    word_id = db.Column(db.ForeignKey('word.id'))
    user_id = db.Column(db.ForeignKey('user.id'))
    # attribute :words: backrefed by Word
    # attribute :users: backrefed by User

    def __init__(self, content):
        self.content = content


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

"""
Note:    Note.users
User:    User.notes  backref='users'
Word:    Word.notes
"""
