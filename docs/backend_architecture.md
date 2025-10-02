# Backend Architecture Overview

This document describes the backend structure, including modules, extensions, and endpoint registration. Update it whenever new packages, blueprints, or data access layers are introduced.

## Directory Layout
```
backend/
├── app/
│   ├── __init__.py        # Application factory
│   ├── config.py          # Environment configuration
│   ├── extensions.py      # Flask extension initialization (JWT, Mongo)
│   └── routes/
│       └── __init__.py    # Blueprint definitions (healthcheck scaffold)
├── requirements.txt       # Backend dependencies
└── wsgi.py                # Entry point for local development
```

## Application Factory
`create_app` loads configuration from `Config`, initializes shared extensions, and registers blueprints. All future modules should expose a `register_<component>` function invoked inside the factory to keep the startup sequence explicit.

## Configuration
`Config` centralizes environment variables for secrets, MongoDB, and JWT settings. Add new configuration values here and document them in [development_environment.md](development_environment.md).

## Extensions
`extensions.py` defines singletons for JWT and MongoDB. Additional services (e.g., Celery, caching) should also be registered here with helper functions to attach them to the Flask app.

## Routes
The healthcheck blueprint is located under `app/routes`. Future blueprints should live in submodules (e.g., `app/routes/buylist.py`) and be registered by updating `register_blueprints`.

## Data Access
Direct MongoDB access is currently provided through `flask_pymongo.PyMongo`. Phase 1 will introduce repository abstractions documented alongside the relevant models.

## Testing Strategy
Unit tests will target blueprints and services using Flask's test client. Integration tests will spin up a test database via fixtures once CI is configured.

## Related Documents
- [Development Environment Setup](development_environment.md)
- [Database Collections & Models](database_models.md)
- [Backend Endpoints](backend_endpoints.md)
