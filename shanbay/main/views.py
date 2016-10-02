# coding=utf-8
from flask import render_template, flash, Markup, redirect, url_for, current_app, request
from . import bp
from flask_login import current_user, login_required
from ..models import User, Note, Word
from itsdangerous import JSONWebSignatureSerializer
from .. import db


@bp.route('/', methods=['GET', 'POST'])
def index():
    if current_user.is_authenticated:
        name = current_user.username
        if request.method == 'GET':
            user = User.query.filter_by(username=name).first()
            is_new_user = user.new_user
            if is_new_user:
                flash(Markup('你是新新新新, 新来的吧, 来<a href="/settings">设置</a>每日计划吧'))

            return render_template('main/index.html', name=name)
        else:
            data = request.form
            words_per_day = data['words_per_day']
            return render_template('main/index.html', name=name, words_per_day=words_per_day)
    else:
        return render_template('main/index.html', name='there')


@bp.route('/review', methods=['GET', 'POST'])
@login_required
def review():
    if current_user.is_authenticated:
        username = current_user.username

        # generate token for authenticating user
        s = JSONWebSignatureSerializer('token', salt=current_app.config['SECRET_KEY'])
        token = s.dumps({'username': username})
        token = token.decode()

        user = User.query.filter_by(username=username).first()
        words_per_day = user.words_per_day
        words = user.words.limit(words_per_day).all()
        return render_template('main/review.html', words=words, token=token, words_per_day=words_per_day)
    else:
        return redirect(url_for('account.login'))


@bp.route('/submit_note', methods=['POST', 'GET'])
def submit_note():
    if request.method == 'POST':
        s = JSONWebSignatureSerializer('token', salt=current_app.config['SECRET_KEY'])
        data = request.form
        note_content = data['note']
        word_id = data['word_id']
        token = data['user_id']

        username = s.loads(token)['username']

        word = Word.query.get(word_id)
        user = User.query.filter_by(username=username).first()
        note = Note(content=note_content)

        user.notes.append(note)
        word.notes.append(note)

        for t in (word, user, note):
            db.session.add(t)
        db.session.commit()
    return redirect(url_for('main.review'))


@bp.route('/words_known')
@bp.route('/words_known/<int:page>')
def words_known(page=1):
    user = User.query.filter_by(username=current_user.username).first()
    words_known = user.words_known.paginate(page, 10, False)
    return render_template('main/words_known.html',
                            user=user,
                            words_known=words_known)


@bp.route('/words_unknown')
@bp.route('/words_unknown/<int:page>')
def words_unknown(page=1):
    user = User.query.filter_by(username=current_user.username).first()
    words_unknown = user.words.paginate(page, 10, False)

    return render_template('main/words_unknown.html', 
                           user=user,
                           words_unknown=words_unknown)
