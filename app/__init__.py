from flask import Flask
from dotenv import load_dotenv
import os

load_dotenv()


def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "secret"
    app.config["HUNTER_API_KEY"] = os.getenv("HUNTER_API_KEY")
    app.config["RECAPTCHA_PUBLIC_KEY"] = os.getenv("RECAPTCHA_V3_PUBLIC_KEY")
    app.config["RECAPTCHA_SECRET_KEY"] = os.getenv("RECAPTCHA_V3_SECRET_KEY")

    from app.routes import index_routes_bp

    app.register_blueprint(index_routes_bp)

    return app
