# coding=utf-8
from flask import render_template, request, redirect, url_for, flash
from .forms import SignupForm, LoginForm, SettingsForm
from . import bp
from ..models import User, Word
from .. import db
from flask_login import login_user, logout_user, login_required, current_user


@bp.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if request.method == 'POST':
        username = form.username.data
        email = form.email.data
        password = form.password.data

        user = User(username=username,
                    email=email,
                    password=password)

        db.session.add(user)
        db.session.commit()
        return redirect(url_for('account.login'))
    return render_template('account/signup.html', form=form)


@bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            user = User.query.filter_by(username=form.username.data).first()
            if user is not None and user.verify_password(form.password.data):
                login_user(user, form.remember_me.data)
                return redirect(url_for('main.index'))
    return render_template('account/login.html', form=form)


@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))


@bp.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    form = SettingsForm()
    if form.validate_on_submit():
        words_per_day = form.words_per_day.data
        category = form.category.data
        user = User.query.filter_by(username=current_user.username).first()

        user.words_per_day = words_per_day
        user.category = category
        user.new_user = 0
        # 添加目标单词到库中
        user.words = Word.query.filter_by(category=category)
        db.session.add(user)
        db.session.commit()
        flash('新的一天从背蛋池开始')
        return redirect(url_for('main.index'))
    return render_template('account/settings.html', form=form)
