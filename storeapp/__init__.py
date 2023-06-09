from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import secrets,os
from flask_login import LoginManager
from flask_mail import Mail
from storeapp.config import Config


db = SQLAlchemy()
migrate=Migrate()
mail=Mail()
login_manager=LoginManager()
login_manager.login_view='users.login' # type: ignore

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    migrate.init_app(app,db)
    mail.init_app(app)
    login_manager.init_app(app)

    from storeapp.users.views import users
    from storeapp.main.views import main
    from storeapp.products.views import product
    from storeapp.seller.views import sellers

    app.register_blueprint(users)
    app.register_blueprint(main)
    app.register_blueprint(product)
    app.register_blueprint(sellers)

    return app







