import logging

from flask import Flask

from app.routes.products import products_bp


def create_app() -> Flask:
    """Create the Flask app for the products assignment."""
    logging.basicConfig(level=logging.INFO, format="%(levelname)s:%(name)s:%(message)s")
    logging.getLogger("app.cache.memory_cache").setLevel(logging.INFO)

    app = Flask(__name__)
    app.register_blueprint(products_bp)

    return app
