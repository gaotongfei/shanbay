from flask import render_template, flash, Markup, redirect, url_for
from . import bp
from flask_login import current_user, login_required
from ..models import User


@bp.route('/', methods=['GET', 'POST'])
def index():
    if current_user.is_authenticated:
        name = current_user.username
        user = User.query.filter_by(username=name).first()
        is_new_user = user.new_user
        if is_new_user:
            flash(Markup('你是新新新新, 新来的吧, 来<a href="/settings">设置</a>每日计划吧'))
    else:
        name = "there"
    return render_template('main/index.html', name=name)


@bp.route('/review', methods=['GET', 'POST'])
@login_required
def review():
    if current_user.is_authenticated:
        user = User.query.filter_by(username=current_user.username).first()
        words_per_day = user.words_per_day
        words = user.words.limit(words_per_day).offset(words_per_day).all()
        print([word.id for word in words])
        print(len(words))
    else:
        return redirect(url_for('account.login'))
    return render_template('main/review.html', words=words)
