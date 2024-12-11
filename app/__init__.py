#################
#### imports ####
#################

import os

from flask import Flask
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mailman import Mail

load_dotenv()

########################
#### instanciations ####
########################

db = SQLAlchemy()
csrf = CSRFProtect()
migrate = Migrate()
mail = Mail()
login_manager = LoginManager()


def create_app():

    ################
    #### config ####
    ################

    app = Flask(__name__)
    app.config.from_object(os.getenv("APP_SETTINGS"))

    ####################
    #### extensions ####
    ####################

    db.init_app(app)
    csrf.init_app(app)
    migrate.init_app(app, db)
    mail.init_app(app)
    login_manager.init_app(app)

    #####################
    #### flask-login ####
    #####################

    login_manager.login_view = "home_routes.login"
    login_manager.login_message = "Por favor inicia sessión para acceder a esta página."
    login_manager.login_message_category = "info"

    @login_manager.user_loader
    def load_user(user_id):
        from app.models import User

        return db.session.get(User, int(user_id))

    ####################
    #### blueprints ####
    ####################

    from app.routes import home_routes_bp
    from app.routes import error_routes_bp
    from app.routes import main_routes_bp
    from app.routes import login_routes_bp

    app.register_blueprint(home_routes_bp)
    app.register_blueprint(error_routes_bp)
    app.register_blueprint(main_routes_bp)
    app.register_blueprint(login_routes_bp)

    return app
