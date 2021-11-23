from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_cors import CORS
from flask_wtf import CSRFProtect
from os.path import join, dirname, realpath
from datetime import timedelta
from yaml import load, Loader
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from logging.handlers import RotatingFileHandler
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)
formatter = logging.Formatter('%(asctime)s:%(name)s:%(message)s')
file_handler = RotatingFileHandler('logs/flask-mini-cms.log', maxBytes=1000000, backupCount=5)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

#temp
logger.error("Inited")

with open(join(dirname(realpath(__file__)), 'config.yaml')) as conf:
    config = load(conf, Loader=Loader)

db = SQLAlchemy()
csrf = CSRFProtect()
limiter = Limiter(key_func=get_remote_address, default_limits=['200 per hour'])

def create_app():
    app = Flask(__name__)

    limiter.init_app(app)

    app.config['SECRET_KEY'] = '0L0O8nl6RFHNgsmB2uB3ld4G9DYgg5fA'
    app.config['SQLALCHEMY_DATABASE_URI'] = config.get('sqlite').get('db')
    app.config['CORS_ORIGINS'] = '*'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    CORS(app)
    csrf.init_app(app)
    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.needs_refresh_message = (u"Session timedout, please re-login")
    login_manager.init_app(app)

    app.permanent_session_lifetime = timedelta(hours=12)

    from .models import User
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .users import users as users_blueprint
    app.register_blueprint(users_blueprint)

    from .posts import posts as posts_blueprint
    app.register_blueprint(posts_blueprint)

    from .errors import errors as errors_blueprint
    app.register_blueprint(errors_blueprint)

    from .img import img as img_blueprint
    app.register_blueprint(img_blueprint)

    from .public import public as public_blueprint
    app.register_blueprint(public_blueprint)

    from .languages import languages as languages_blueprint
    app.register_blueprint(languages_blueprint)

    with app.app_context(): 
        try:
            user = User.query.first()
            if user:
                return app
        except:
            try:
                db.create_all()
            except Exception as ex:
                print(ex)
    return app
    