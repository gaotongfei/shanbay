from . import bp
from ..models import User
from flask_login import current_user


@bp.route('/api/is_new')
def index():
    user = current_user.username
    user = User.query.filter_by(username=user).first()
    is_new_user = user.new_user
    print(is_new_user)
    return 'api test'
