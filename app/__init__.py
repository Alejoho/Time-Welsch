from flask import Flask
from dotenv import load_dotenv
import os
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mailman import Mail
from itsdangerous import URLSafeTimedSerializer

load_dotenv()

db = SQLAlchemy()
csrf = CSRFProtect()
migrate = Migrate()
mail = Mail()
login_manager = LoginManager()


def create_app():
    # TODO: Load the configuration from an object
    app = Flask(__name__)
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
    app.config["SECURITY_PASSWORD_SALT"] = os.getenv("SECURITY_PASSWORD_SALT")
    app.config["HUNTER_API_KEY"] = os.getenv("HUNTER_API_KEY")
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")

    app.config["RECAPTCHA_PUBLIC_KEY"] = os.getenv("RECAPTCHA_PUBLIC_KEY")
    app.config["RECAPTCHA_PRIVATE_KEY"] = os.getenv("RECAPTCHA_PRIVATE_KEY")

    app.config["MAIL_SERVER"] = os.getenv("MAIL_SERVER")
    app.config["MAIL_PORT"] = os.getenv("MAIL_PORT")
    app.config["MAIL_USE_TLS"] = os.getenv("MAIL_USE_TLS")
    app.config["MAIL_USERNAME"] = os.getenv("MAIL_USERNAME")
    app.config["MAIL_PASSWORD"] = os.getenv("MAIL_PASSWORD")

    # TODO: Put the serializer in the file where its use
    serializer = URLSafeTimedSerializer(app.config["SECRET_KEY"])
    app.config["SERIALIZER"] = serializer

    db.init_app(app)
    csrf.init_app(app)
    migrate.init_app(app, db)
    mail.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = "home_routes.login"

    # LATER: Use the new way of sqlalchemy to query the db
    @login_manager.user_loader
    def load_user(user_id):
        from app.models import User

        return User.query.get_or_404(int(user_id))

    from app.routes import home_routes_bp

    app.register_blueprint(home_routes_bp)

    # TODO: Add error pages

    return app
