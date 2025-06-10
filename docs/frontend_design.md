# Frontend Design Overview

This document summarizes the design, structure, and key considerations for the Interview Questions App frontend.

## Technology Stack

- **Framework:** React (with functional components and hooks)
- **UI Library:** Material UI (MUI)
- **Build Tool:** Vite (for fast development and HMR)
- **State Management:** Local component state (React hooks)
- **API Communication:** Axios (via `api.js`)

## Structure

- All frontend code is under the `frontend/` directory.
- Main entry point: `src/main.jsx` and `src/App.jsx`.
- Components are organized in `src/components/`:
  - `QuestionList.jsx`: List, add, edit, delete questions; manage tags; filter and display question details.
  - `QuestionLogList.jsx`: View and manage logs/attempts for each question.
  - `TagList.jsx`: Manage tags (CRUD) and tag assignment to questions.
- Global styles in `src/index.css` and `src/App.css`.

## Key Features & Flows

- **Question Management:**
  - Users can view, add, edit, and delete questions.
  - Questions can be tagged and filtered by tags or difficulty.
  - Each question can be marked active/inactive.

- **Log/Attempt Management:**
  - Users can view and manage logs (attempts) for each question.
  - Each log records date, time spent, outcome, approach, and notes.

- **Tag Management:**
  - Users can create, edit, and delete tags.
  - Tags can be assigned to questions for organization and filtering.

- **Import Flow:**
  - Users can import their activity from supported coding platforms (e.g., Codewars) via a dedicated UI flow.
  - The frontend sends a POST request to the backend import API and displays results or errors.

- **Navigation:**
  - Uses React Router for navigation between question list and log views.
  - AppBar provides quick access to main sections.

## Concerns & Best Practices

- **Responsiveness:**
  - Uses Material UI's responsive components and layout utilities for a good experience on all devices.

- **Error Handling:**
  - API errors are caught and can be surfaced to the user (e.g., via dialogs or notifications).

- **Performance:**
  - Data is fetched on mount and after CRUD actions to keep the UI in sync.
  - Loading indicators (e.g., CircularProgress) are shown during API calls.

- **Extensibility:**
  - Component-based structure makes it easy to add new features or views.
  - API endpoints and flows are abstracted in `api.js` for maintainability.

## Development

- Start the frontend with `npm run dev` in the `frontend/` directory.
- Linting and formatting are configured via ESLint and Prettier.
- See `frontend/README.md` for more details on local setup.

---

For more details on backend and API, see the documentation in the `docs/` directory at the project root.
