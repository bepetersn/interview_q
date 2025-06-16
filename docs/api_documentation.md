# API Documentation

This project uses **drf-spectacular** to generate OpenAPI documentation.

## Accessing the Docs

- **Schema (JSON):** `http://127.0.0.1:8000/api/schema/`
- **Swagger UI:** `http://127.0.0.1:8000/api/docs/`

Run the Django development server and visit the above URLs in your browser to view the OpenAPI schema or interactive UI.

## Updating the Schema

1. Ensure new endpoints include proper DRF serializer and view definitions.
2. The schema is generated dynamically at runtime. No manual steps are required after updating code.
3. If you change global settings, update `SPECTACULAR_SETTINGS` in `backend/settings.py`.

To install missing dependencies, run:

```bash
pip install -r requirements.txt
```

---

## API Endpoints

### Authentication
- `POST /api/accounts/register/` — Register a new user (username, password)
- `POST /api/accounts/login/` — Log in and obtain a session
- `GET /api/accounts/identity/` — Get info about the currently authenticated user -- does NOT require authentication.

### Questions
- `GET /api/questions/` — List all questions for the authenticated user
- `POST /api/questions/` — Create a new question
- `GET /api/questions/<id>/` — Retrieve a specific question
- `PUT /api/questions/<id>/` — Update a question
- `PATCH /api/questions/<id>/` — Partially update a question
- `DELETE /api/questions/<id>/` — Delete a question and its logs

### Question Logs
- `GET /api/questions/<questionId>/logs/` — List all logs for a question
- `POST /api/questions/<questionId>/logs/` — Create a new log for a question
- `GET /api/questions/<questionId>/logs/<logId>/` — Retrieve a specific log
- `PUT /api/questions/<questionId>/logs/<logId>/` — Update a log
- `PATCH /api/questions/<questionId>/logs/<logId>/` — Partially update a log
- `DELETE /api/questions/<questionId>/logs/<logId>/` — Delete a log

### Tags
- `GET /api/tags/` — List all tags for the authenticated user
- `POST /api/tags/` — Create a new tag
- `GET /api/tags/<id>/` — Retrieve a specific tag
- `PUT /api/tags/<id>/` — Update a tag
- `PATCH /api/tags/<id>/` — Partially update a tag
- `DELETE /api/tags/<id>/` — Delete a tag

### Import API (planned/future)
- See `docs/features/import_api_design.md` for planned endpoints to import question logs from external platforms.

---

All endpoints require authentication unless otherwise noted. Most endpoints operate only on data belonging to the logged-in user. See the Swagger UI for full details on request/response schemas and additional query parameters.
