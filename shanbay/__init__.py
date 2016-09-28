from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from .config import config


db = SQLAlchemy()
bootstrap = Bootstrap()
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'account.login'


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    db.init_app(app)
    bootstrap.init_app(app)
    login_manager.init_app(app)

    from .main import bp as main_bp
    app.register_blueprint(main_bp)

    from .account import bp as account_bp
    app.register_blueprint(account_bp)

    from .api import bp as api_bp
    app.register_blueprint(api_bp)

    return app
