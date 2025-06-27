# Interview Questions App

This project is a full-stack application for managing programming interview questions and activity logs. It is designed to help users track their practice, import progress from coding platforms, and organize questions and tags for efficient interview preparation.

## Overview

- **Backend:**
  - Built with Django and Django REST Framework (DRF).
  - Provides a RESTful API for managing questions, tags, and user activity logs.
  - Planned support for importing question logs from external coding platforms (see `docs/import_api_design.md`).
  - Includes robust testing, data seeding, and admin customization.
  - See `docs/backend_design.md` and `docs/import_api_design.md` for detailed backend and API design.

- **Frontend:**
  - Built with React and Material UI, using Vite for fast development.
  - Allows users to view, add, edit, and delete questions, tags, and logs.
  - Supports tag management and question filtering.
  - A user-friendly import interface is planned once backend support is implemented.

## Getting Started

- **Backend:**
  - Install dependencies from `requirements.txt`.
  - Run migrations and seed data with `python manage.py create_fake_data`.
  - Start the server with `python manage.py runserver`.

- **Frontend:**
  - Navigate to the `frontend/` directory.
  - Install dependencies with `npm install`.
  - Start the development server with `npm run dev`.

## Monitoring with Sentry

To enable Sentry monitoring, create Sentry projects for both the backend and the
frontend and set the following environment variables:

- `BACKEND_SENTRY_DSN` for the Django backend
- `VITE_FRONTEND_SENTRY_DSN` for the React frontend

With these variables set, both applications will send errors and performance
data to Sentry.

## Documentation

- Backend architecture: [`docs/backend_design.md`](docs/backend_design.md)
- Import API design: [`docs/import_api_design.md`](docs/import_api_design.md)

## Contributing

- Review the backend and API documentation in the `docs/` directory.
- See the Playwright and Django tests in `apps/core/tests` for usage examples.
- For admin or data model changes, check the `apps/core` and `apps/q_admin` directories.

---

For more details on backend structure, configuration, and contributor notes, see the documentation in the `docs/` directory.
