from flask import render_template, flash, Markup
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
        print(user.selected_words)
        print(user.words_per_day)
    return render_template('main/review.html')
