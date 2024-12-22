# LATER: Document the majority of the code posible
# LATER: Validate all pages with the cs50 validator

#################
#### imports ####
#################

import os

from dotenv import load_dotenv
from flask import Flask
from flask_login import LoginManager
from flask_mailman import Mail
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from sqlalchemy import select

load_dotenv()

########################
#### instanciations ####
########################

db = SQLAlchemy()
csrf = CSRFProtect()
migrate = Migrate()
mail = Mail()
login_manager = LoginManager()
chapters = []


def create_app():

    ################
    #### config ####
    ################

    app = Flask(__name__)
    app.config.from_object(os.getenv("APP_SETTINGS"))
    app.jinja_env.trim_blocks = True
    app.jinja_env.lstrip_blocks = True

    ####################
    #### extensions ####
    ####################

    db.init_app(app)
    csrf.init_app(app)
    migrate.init_app(app, db)
    mail.init_app(app)
    login_manager.init_app(app)

    from app.models import Chapter

    with app.app_context():
        global chapters
        chapters = db.session.scalars(select(Chapter).order_by(Chapter.number)).all()

    #####################
    #### flask-login ####
    #####################

    login_manager.login_view = "login_routes.login"
    login_manager.login_message = "Por favor inicia sessión para acceder a esta página."
    login_manager.login_message_category = "info"

    # TODO: Change the user_loader to inside the User model
    @login_manager.user_loader
    def load_user(user_id):
        from app.models import User

        return db.session.get(User, int(user_id))

    ####################
    #### blueprints ####
    ####################

    from app.routes import (
        error_routes_bp,
        home_routes_bp,
        login_routes_bp,
        main_routes_bp,
        register_routes_bp,
        settings_routes_bp,
    )

    app.register_blueprint(home_routes_bp)
    app.register_blueprint(error_routes_bp)
    app.register_blueprint(main_routes_bp)
    app.register_blueprint(login_routes_bp)
    app.register_blueprint(register_routes_bp)
    app.register_blueprint(settings_routes_bp)

    return app
