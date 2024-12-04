from flask import Flask
from dotenv import load_dotenv
import os

load_dotenv()


def create_app():

    app = Flask(__name__)
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

    from app.routes import home_routes_bp

    app.register_blueprint(home_routes_bp)

    return app