# Development Environment Setup

This document outlines the tooling required to build and run BuyLyst locally. Every time a new dependency or tool is introduced, update this guide and reference it from relevant TODO items.

## Prerequisites
- **Python 3.11** (backend services)
- **Node.js 20.x** and **npm 10+** (frontend build tooling, to be added in later phases)
- **MongoDB 6.x** running locally or accessible via URI
- **Redis** (planned for job queue/backfill work in later phases)
- **Poetry 1.7+** or `pip` for managing backend dependencies (currently using `requirements.txt` for the Flask scaffold)

## Environment Variables
Set the following environment variables when running the backend:

| Variable | Description | Default |
|----------|-------------|---------|
| `BUYLYST_SECRET_KEY` | Flask secret key | `dev-secret-change-me` |
| `BUYLYST_MONGO_URI` | MongoDB connection string | `mongodb://localhost:27017/buylyst` |
| `BUYLYST_JWT_SECRET` | JWT signing secret | Falls back to `BUYLYST_SECRET_KEY` |
| `FLASK_ENV` | Flask environment flag | `development` |

## Backend Setup Steps
1. `cd backend`
2. Create a virtual environment: `python -m venv .venv`
3. Activate the environment: `source .venv/bin/activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Export environment variables (see above).
6. Launch the development server: `flask --app wsgi run --debug`

The current backend exposes a healthcheck at `GET /api/health/`. Additional endpoints will be added per the implementation plan.

## Frontend Setup (Placeholder)
Frontend scaffolding is not yet committed. Once created, this section will document the React project structure, dependency installation, and development commands.

## Tooling Notes
- Use `pre-commit` hooks (to be configured in upcoming tasks) for linting and formatting enforcement.
- Docker compose definitions will be introduced once services beyond MongoDB are required.

## References
- [Backend Architecture Overview](backend_architecture.md)
- [Implementation Plan](implementation_plan.md)
