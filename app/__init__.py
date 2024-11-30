from flask import Flask
from itsdangerous import URLSafeTimedSerializer
from dotenv import load_dotenv
import os

load_dotenv()
# TODO: Ask copilot if i can do with the serializer what I do with the sqlachemy, migrate, and flask_login packages


def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "secret"
    app.config["HUNTER_API_KEY"] = os.getenv("HUNTER_API_KEY")
    serializer = URLSafeTimedSerializer(app.config["SECRET_KEY"])
    app.config["SERIALIZER"] = serializer

    from app.routes import index_routes_bp

    app.register_blueprint(index_routes_bp)

    return app
