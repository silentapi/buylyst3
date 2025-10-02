"""Extension registry for the BuyLyst backend."""
from __future__ import annotations

from flask import Flask
from flask_jwt_extended import JWTManager
from flask_pymongo import PyMongo

jwt = JWTManager()
mongo = PyMongo()


def init_extensions(app: Flask) -> None:
    """Bind shared extensions to the provided Flask app."""
    jwt.init_app(app)
    mongo.init_app(app)
