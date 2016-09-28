from flask import render_template
from . import bp
from flask_login import current_user


@bp.route('/', methods=['GET', 'POST'])
def index():
    name = current_user.username
    return render_template('main/index.html', name=name)
