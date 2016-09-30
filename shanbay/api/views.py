from flask import request, current_app, abort
from . import bp
from ..models import User, Word
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

            print(word.word)
            print(word.category)
            print(word.translation)

            # add current word to user known words
            user.words_known.append(word)
            # delete current word from reviewing task
            user.words.remove(word)

            db.session.add(user)
            db.session.commit()
    else:
        abort(404)

    return 'success'
