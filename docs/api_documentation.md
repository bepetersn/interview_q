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
