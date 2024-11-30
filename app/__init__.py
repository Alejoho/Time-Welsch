from flask import Flask


def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "secret"

    from app.routes import index_routes_bp

    app.register_blueprint(index_routes_bp)

    return app
