# Interview Questions API

This repository contains a small Django REST project for managing interview questions and activity logs. Below is an overview originally provided in conversation with an assistant.

**General Structure**

- **Django project root** with common entry points:
  - `manage.py` for command‑line tasks
  - `asgi.py` and `wsgi.py` to expose ASGI/WGI apps
  - `settings.py` defines installed apps, middleware and other configuration
  - `urls.py` routes the Django admin and the project’s API endpoints

- **Apps**
  - `apps/core`: main REST API
    - Models `Tag`, `Question` and `QuestionLog` store questions and activity logs
    - Serializers map these models to JSON for the API
    - Views implement CRUD endpoints using Django REST Framework generics and viewsets
    - `urls.py` wires the view classes and viewsets
    - `management/commands/create_fake_data.py` provides a custom command to populate test data
    - Extensive tests under `apps/core/tests` exercise the API via Playwright using parametrized fixtures

  - `apps/q_admin`: intended for Django admin customizations but currently contains only `admin.py` registering a simple admin class

- **Additional directories**
  - `q_admin/` at the project root includes admin code that mirrors the app folder; its purpose may overlap with `apps/q_admin`.

- **Configuration files**
  - `requirements.txt` lists runtime dependencies (Django, DRF, Playwright, etc.)
  - `pyproject.toml` configures Black formatting exclusions
  - `conftest.py` initializes Django for tests and loads fixtures from `apps.core.tests.fixtures`

**Important Things to Know**

- It’s a Django REST Framework project designed to track programming interview questions and logs. Core endpoints operate under `/api/` as routed in `urls.py`.
- Tests make HTTP requests with Playwright rather than Django’s test client, so they depend on an actual server. The fixtures reset the SQLite database after each test.
- A custom management command (`create_fake_data`) can be used to seed the database.
- Logging is configured via the `LOGGING` dictionary in `settings.py` to output to console with additional logger settings for `apps.core.views`.

**Pointers for New Contributors**

1. **Understand Django basics and Django REST Framework**—the project leans on DRF’s generics/viewsets for most endpoints.
2. **Examine the tests** under `apps/core/tests` to see how API usage is expected.
3. **Check the admin setup**. `apps.q_admin` is listed in `INSTALLED_APPS`, but `apps/q_admin` lacks an `__init__.py`, so it isn’t a proper package.
4. **Run `create_fake_data`** via `python manage.py create_fake_data` to populate example data for local testing.
5. **Consider cleaning up the admin modules**—decide whether the root `q_admin/` folder or `apps/q_admin/` is the intended location and remove duplicates.

**Possible Follow‑ups**

:::task-stub{title="Fix missing package initialization for q_admin"}
Add an `__init__.py` file in `apps/q_admin/` or adjust `INSTALLED_APPS` if the module isn’t used. Ensure Django can import the admin customizations properly.
:::

:::task-stub{title="Remove or consolidate duplicate q_admin directories"}
Determine whether `q_admin/admin.py` at the project root or `apps/q_admin/admin.py` is the correct implementation. Remove the unused folder and update imports accordingly.
:::
