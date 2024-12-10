from flask import Flask
from dotenv import load_dotenv
import os
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mailman import Mail

load_dotenv()

db = SQLAlchemy()
csrf = CSRFProtect()
migrate = Migrate()
mail = Mail()
login_manager = LoginManager()


def create_app():
    # TODO: Load the configuration from an object
    app = Flask(__name__)
    app.config.from_object(os.getenv("APP_SETTINGS"))

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
    from app.routes import error_routes_bp
    from app.routes import main_routes_bp

    app.register_blueprint(home_routes_bp)
    app.register_blueprint(error_routes_bp)
    app.register_blueprint(main_routes_bp)

    return app
