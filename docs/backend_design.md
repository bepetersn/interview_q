# Backend Design Overview

**Django project root** with common entry points:
  - `manage.py` for command‑line tasks (with optional Datadog APM auto-instrumentation)
  - `backend/asgi.py` and `backend/wsgi.py` to expose ASGI/WSGI apps (with optional Datadog APM support)
  - `backend/settings.py` defines installed apps, middleware and other configuration
  - `backend/urls.py` routes the API schema documentation and project's API endpointsesign Overview

This document describes the backend architecture and design for the Interview Questions API project.

## General Structure

- **Django project root** with common entry points:
  - `manage.py` for command‑line tasks
  - `asgi.py` and `wsgi.py` to expose ASGI/WGI apps
  - `settings.py` defines installed apps, middleware and other configuration
  - `urls.py` routes the Django admin and the project’s API endpoints

- **Backend**
  - `backend/core`: main REST API
    - Models `Tag`, `Question` and `QuestionLog` store questions and activity logs, all linked to user accounts
    - Serializers map these models to JSON for the API
    - Views implement CRUD endpoints using Django REST Framework generics and viewsets
    - `urls.py` wires the view classes and viewsets
    - `management/commands/create_fake_data.py` provides a custom command to populate test data
    - Extensive tests under `backend/core/tests` exercise the API using parametrized fixtures

  - `backend/accounts`: user authentication and management
    - Provides user registration, login, logout, and identity endpoints
    - Handles session-based authentication
    - URLs are mounted under `/api/accounts/`

- **Additional directories**
  - `backend/test_common/`: shared test fixtures and utilities
  - `backend/db/`: database-related files and migrations
  - `backend/aws.py`: AWS-specific configuration (likely for deployment)

- **Configuration files**
  - `requirements.txt` lists runtime dependencies (Django, DRF, PostgreSQL drivers, etc.)
  - `requirements.in` defines the core dependencies (with some merge conflicts to resolve)
  - `pyproject.toml` configures Black formatting exclusions, isort settings, and pytest configuration
  - `conftest.py` initializes Django for tests and loads fixtures from `backend.test_common.fixtures`
  - `.pre-commit-config.yaml` configures code quality and security hooks (Black, Flake8, isort, Bandit, Codespell, PyUpgrade, TruffleHog, etc.)
  - `.env.example` provides environment variable templates for development and production
  - API documentation is generated using `drf-spectacular` with schema available at `/api/schema/` and Swagger UI at `/api/docs/`

## Important Things to Know

- It's a Django REST Framework project designed to track programming interview questions and logs. Core endpoints operate under `/api/` as routed in `backend/urls.py`.
- **Database**: Configured for PostgreSQL in production with fallback to local SQLite for development
- **Authentication**: Session-based authentication is implemented. All core endpoints require authentication and operate only on user-owned data.
- Integration tests make HTTP requests rather than Django's test client, so they depend on an actual server. The fixtures reset the database after each test.
- A custom management command (`create_fake_data`) can be used to seed the database.
- Logging is configured via the `LOGGING` dictionary in `settings.py` to output to console with additional logger settings for `backend.core.views`.
- **Security**: Pre-commit hooks are set up for code formatting, linting, security, and secret scanning. Bandit is configured to only fail for issues at or above high severity, and to exclude test and utility directories from scans.
- **APM**: Optional Datadog APM instrumentation is supported. When `DD_TRACE_ENABLED=true` is set and the `ddtrace` package is installed, start the server with `python -m ddtrace run manage.py runserver` to automatically trace Django requests.
- **CORS**: Configured for cross-origin requests to support frontend-backend communication
- **Static Files**: Configured to serve frontend assets using WhiteNoise middleware
- **API Documentation**: Auto-generated using drf-spectacular, accessible at `/api/docs/` for Swagger UI and `/api/schema/` for JSON schema

## Deletion Endpoints

Just as an FYI, the API supports deleting questions, logs and tags via REST calls:

- `DELETE /api/questions/<id>/` removes a question and any related `QuestionLog` records.
- `DELETE /api/questions/<question_id>/logs/<id>/` removes a single log entry.
- `DELETE /api/tags/<id>/` removes a tag.

These routes are covered by the tests in `backend/core/tests` to verify proper database cleanup is always done.

## Authentication Workflow

The API now requires a logged‑in user for all core endpoints.
- Users can be created via `/api/accounts/register/` by POSTing a `username` and `password`.
- To obtain a session, POST the same credentials to `/api/accounts/login/`.
- After logging in, requests to `/api/questions/`, `/api/questions/<question_id>/logs/` and `/api/tags/` will operate only on data belonging to that user.
- The `/api/accounts/identity/` endpoint returns information about the currently authenticated user. When accessed with a valid session or authentication token, it responds with user details such as username and user ID. This is useful for client applications to confirm the logged-in user's identity and display relevant account information. The browser is expected to send sessionid credentials (`withCredentials`).

## API Endpoints Structure

The API is organized as follows:

### Core Endpoints (Authentication Required)
- **Questions**: `/api/questions/` - Full CRUD operations via ViewSet
- **Question Logs**: `/api/questions/<question_id>/logs/` - Nested under questions for better organization
- **Tags**: `/api/tags/` - List/Create and detail operations via generic views

### Authentication Endpoints
- `/api/accounts/register/` - User registration
- `/api/accounts/login/` - User login (creates session)
- `/api/accounts/logout/` - User logout
- `/api/accounts/identity/` - Get current user information

### Documentation
- `/api/schema/` - OpenAPI JSON schema
- `/api/docs/` - Interactive Swagger UI documentation

All core endpoints are scoped to the authenticated user's data automatically.

## Possible Follow-ups

- **Enhanced admin interface**: Expand the Django admin with proper registration for Question and QuestionLog models
- **Switch to using Poetry**: It's troublesome managing requirements.txt and requirements.in without it.
- **Import API implementation**: Build the planned import endpoints for external platforms (see `docs/features/import_api_design.md`)
- **Background processing**: Add for async operations like imports, using AWS
- **Performance optimization**: Add database indexing, query optimization, and caching where needed
