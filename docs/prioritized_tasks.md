# Prioritized Task Breakdown

This document organizes the ideas from `future_concerns.md` into actionable tasks with a rough priority order.

## Priority 1 – Core Foundations
- **User Authentication & Authorization**
  - Add backend user accounts and authentication (JWT or session based).
  - Scope questions and logs to the authenticated user.
  - Implement login/registration flows in the frontend.
- **Import API Implementation & Background Jobs**
  - Build the import API endpoints for supported coding platforms.
  - Create a background task system so imports can run asynchronously.
  - Add rate limiting to keep upstream services happy.
- **Frontend Test Coverage**
  - Set up Jest/React Testing Library for component tests.

## Priority 2 – Usability & Documentation
- **Error Feedback & Onboarding**
  - Standardize toast/inline error messages across the UI.
  - Provide onboarding or help tips for the import feature.
- **State Management & Accessibility**
  - Evaluate a global state manager (Redux, Zustand, or Context) if the app grows.
  - Audit UI components for ARIA labels and keyboard navigation.
- **API Documentation**
  - Publish OpenAPI/Swagger docs for the backend.
- **Deployment & CI/CD**
  - Document or automate deployment steps (Docker, GitHub Actions).
- **Data Privacy**
  - Clarify how user data is stored and deleted; draft a privacy policy.

## Priority 3 – Future Enhancements
- Support more coding platforms in the import API.
- Add advanced filtering, search, and analytics in the frontend.
- Improve admin and moderation tools for managing questions and logs.
- Enhance user profile and progress tracking features.
