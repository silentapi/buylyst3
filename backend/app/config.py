"""Configuration management for the BuyLyst backend."""
from __future__ import annotations

import os
from datetime import timedelta


class Config:
    """Default configuration values for all environments."""

    SECRET_KEY: str = os.environ.get("BUYLYST_SECRET_KEY", "dev-secret-change-me")
    MONGO_URI: str = os.environ.get("BUYLYST_MONGO_URI", "mongodb://localhost:27017/buylyst")

    JWT_SECRET_KEY: str = os.environ.get("BUYLYST_JWT_SECRET", SECRET_KEY)
    JWT_ACCESS_TOKEN_EXPIRES: timedelta = timedelta(minutes=30)

    SCHEDULER_API_ENABLED: bool = False
    ENV: str = os.environ.get("FLASK_ENV", "development")
