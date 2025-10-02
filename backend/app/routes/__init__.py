"""Route blueprints for the BuyLyst backend."""
from __future__ import annotations

from flask import Blueprint, Flask, jsonify

health_bp = Blueprint("health", __name__, url_prefix="/api/health")


@health_bp.get("/")
def healthcheck() -> tuple[dict[str, str], int]:
    """Basic healthcheck endpoint used for readiness probes."""
    return jsonify(status="ok"), 200


def register_blueprints(app: Flask) -> None:
    """Register all application blueprints."""
    app.register_blueprint(health_bp)
