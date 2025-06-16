# Backend Design Overview

This document describes the backend architecture and design for the Interview Questions API project.

## General Structure

- **Django project root** with common entry points:
  - `manage.py` for command‑line tasks
  - `asgi.py` and `wsgi.py` to expose ASGI/WGI apps
  - `settings.py` defines installed apps, middleware and other configuration
  - `urls.py` routes the Django admin and the project’s API endpoints

- **Backend**
  - `backend/core`: main REST API
    - Models `Tag`, `Question` and `QuestionLog` store questions and activity logs
    - Serializers map these models to JSON for the API
    - Views implement CRUD endpoints using Django REST Framework generics and viewsets
    - `urls.py` wires the view classes and viewsets
    - `management/commands/create_fake_data.py` provides a custom command to populate test data
    - Extensive tests under `backend/core/tests` exercise the API using parametrized fixtures

  - `backend/q_admin`: intended for Django admin customizations but currently contains only `admin.py` registering a simple admin class

- **Additional directories**
  - `q_admin/` at the project root includes admin code that mirrors the app folder; its purpose may overlap with `backend/q_admin`.

- **Configuration files**
  - `requirements.txt` lists runtime dependencies (Django, DRF, etc.)
  - `pyproject.toml` configures Black formatting exclusions
  - `conftest.py` initializes Django for tests and loads fixtures from `backend.test_common.fixtures`
  - `.pre-commit-config.yaml` configures code quality and security hooks (Black, Flake8, isort, Bandit, etc.)
  - `bandit.yaml` configures Bandit security scanning (directory exclusions, etc.)

## Important Things to Know

- It’s a Django REST Framework project designed to track programming interview questions and logs. Core endpoints operate under `/api/` as routed in `urls.py`.
- Integration tests make HTTP requests rather than Django’s test client, so they depend on an actual server. The fixtures reset the SQLite database after each test.
- A custom management command (`create_fake_data`) can be used to seed the database.
- Logging is configured via the `LOGGING` dictionary in `settings.py` to output to console with additional logger settings for `backend.core.views`.
- Pre-commit hooks are set up for code formatting, linting, security, and secret scanning. Bandit is configured to only fail for issues at or above a specified severity, and to exclude test and utility directories from scans.

## Deletion Endpoints

The API supports deleting questions, logs and tags via REST calls:

- `DELETE /api/questions/<id>/` removes a question and any related `QuestionLog` records.
- `DELETE /api/questionlogs/<id>/` removes a single log entry.
- `DELETE /api/tags/<id>/` removes a tag.

These routes are covered by the tests in `backend/core/tests` to verify proper database cleanup.

## Possible Follow-ups

- **Fix missing package initialization for q_admin**: Add an `__init__.py` file in `backend/q_admin/` or adjust `INSTALLED_APPS` if the module isn’t used. Ensure Django can import the admin customizations properly.
- **Remove or consolidate duplicate q_admin directories**: Determine whether `q_admin/admin.py` at the project root or `backend/q_admin/admin.py` is the correct implementation. Remove the unused folder and update imports accordingly.

## Authentication Workflow

The API now requires a logged‑in user for all core endpoints.
- Users can be created via `/api/accounts/register/` by POSTing a `username` and `password`.
- To obtain a session, POST the same credentials to `/api/accounts/login/`.
- After logging in, requests to `/api/questions/`, `/api/questionlogs/` and `/api/tags/` will operate only on data belonging to that user.
- The `/api/accounts/identity/` endpoint returns information about the currently authenticated user. When accessed with a valid session or authentication token, it responds with user details such as username and user ID. This is useful for client applications to confirm the logged-in user's identity and display relevant account information. The browser is expected to send sessionid credentials (`withCredentials`).
