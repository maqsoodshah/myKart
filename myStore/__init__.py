from flask import Flask
from myStore.config import Config
from flask_mongoengine import MongoEngine
from mongoengine import connect
from flask_bcrypt import Bcrypt
from flask_mail import Mail
from flask_login import LoginManager
from flask_pymongo import PyMongo
from flask_admin import Admin
from flask_admin.contrib.pymongo import ModelView, filters


mongo = PyMongo()
mail = Mail()
db = MongoEngine()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)
    mongo.init_app(app)
    mail.init_app(app)
    bcrypt.init_app(app)
    connect(db='mykart', username='ma', password='ma123')
    db.init_app(app)
    login_manager.init_app(app)

    from myStore.main.routes import main
    from myStore.users.routes import users
    from myStore.seller.routes import seller
    from myStore.errors.handlers import errors

    app.register_blueprint(main)
    app.register_blueprint(users)
    app.register_blueprint(seller)

    return app
