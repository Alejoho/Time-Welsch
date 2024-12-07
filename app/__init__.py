from flask import Flask
from dotenv import load_dotenv
import os
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from flask_migrate import Migrate
from flask_login import LoginManager

load_dotenv()

db = SQLAlchemy()
csrf = CSRFProtect()
migrate = Migrate()
login_manager = LoginManager()


def create_app():

    app = Flask(__name__)
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
    app.config["HUNTER_API_KEY"] = os.getenv("HUNTER_API_KEY")
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
    app.config["RECAPTCHA_PUBLIC_KEY"] = os.getenv("RECAPTCHA_PUBLIC_KEY")
    app.config["RECAPTCHA_PRIVATE_KEY"] = os.getenv("RECAPTCHA_PRIVATE_KEY")

    db.init_app(app)
    csrf.init_app(app)
    migrate.init_app(app, db)
    # login_manager.init_app(app)
    # login_manager.login_view = "home_routes.login"

    from app.routes import home_routes_bp

    app.register_blueprint(home_routes_bp)

    return app
