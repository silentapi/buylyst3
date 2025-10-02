"""Application factory for the BuyLyst backend."""
from __future__ import annotations

from flask import Flask

from . import routes
from .config import Config
from .extensions import init_extensions


def create_app(config: type[Config] | None = None) -> Flask:
    """Create and configure the Flask application instance."""
    app = Flask(__name__)
    app.config.from_object(config or Config)

    init_extensions(app)
    routes.register_blueprints(app)

    return app
