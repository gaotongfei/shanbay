from flask import render_template, flash, Markup, redirect, url_for, current_app, request
from . import bp
from flask_login import current_user, login_required
from ..models import User
from itsdangerous import JSONWebSignatureSerializer


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

        # flash messages when user complete all words
    else:
        return redirect(url_for('account.login'))
    return render_template('main/review.html', words=words, token=token, words_per_day=words_per_day)
