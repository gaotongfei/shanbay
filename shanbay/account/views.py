from flask import render_template, request, redirect, url_for
from .forms import SignupForm, LoginForm
from . import bp
from ..models import User
from .. import db
from flask_login import login_user, logout_user, login_required, current_user


@bp.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if request.method == 'POST':
        username = form.username.data
        email = form.email.data
        password = form.password.data

        user = User(
            username=username,
            email=email,
            password=password
        )

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


@bp.route('/settings')
def settings():
    return 'settings'
