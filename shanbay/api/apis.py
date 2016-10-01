# coding=utf-8
from flask import request, current_app, abort, jsonify
from . import bp
from ..models import User, Word, Note
from itsdangerous import JSONWebSignatureSerializer
from .. import db


@bp.route('/api/known', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        s = JSONWebSignatureSerializer('token', salt=current_app.config['SECRET_KEY'])
        data = request.form
        if data:
            token = data['token']
            word_id = data['word_id']
            username = s.loads(token)['username']
            user = User.query.filter_by(username=username).first()
            word = Word.query.filter_by(id=word_id).first()

            # add current word to user known words
            user.words_known.append(word)
            # delete current word from reviewing task
            user.words.remove(word)

            db.session.add(user)
            db.session.commit()
    else:
        abort(400)

    return 'success'


@bp.route('/api/load_notes', methods=['GET', 'POST'])
def load_notes():
    """
    load notes of current word
    """
    if request.method == 'POST':
        data = request.form
        word_id = data['word_id']
        notes = Note.query.filter_by(word_id=word_id).all()
        print(notes)
        notes_info = [{'username': note.users.username, 'content': note.content,
                       'created_time': note.created_time} for note in notes]
        return jsonify(word_id=word_id, notes_info=notes_info)
    else:
        abort(400)

