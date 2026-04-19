from flask import Flask

from app.routes.products import products_bp


def create_app() -> Flask:
    """Create the Flask app for the products assignment."""
    app = Flask(__name__)
    app.register_blueprint(products_bp)

    return app
