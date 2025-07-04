# GitHub Copilot Instructions for Interview Questions App

## Project Overview
This is a Django REST Framework backend with React frontend for managing programming interview questions. Focus on code quality, consistency, and comprehensive testing.

## Code Quality Standards

### General Principles
- Follow DRY (Don't Repeat Yourself) principle (not more than 2 times)
- ALMOST ALWAYS use meaningful variable and function names
- Use comments and docstrings to explain complex logic
- Use type annotations where applicable
- Maintain consistent code formatting (PEP 8 for Python, ESLint/Prettier for JavaScript)
- Avoid deeply nested structures -- max ~3-5 levels
- Use early returns and guard statements to simplify control flow
- Use async/await for asynchronous operations in JavaScript
- Use context managers for resource management in Python
- Don't reuse variable names in the same scope
- Minimize state mutations
- Use constants for magic numbers and strings
- Implement single responsibility principle
- Maintain consistent naming conventions
- Prioritize readability and maintainability
- Include comprehensive error handling

### Backend (Django/DRF)
- Use Django best practices for models, views, and serializers
- Implement proper validation and error handling
- Write comprehensive tests for all endpoints
- Use descriptive variable names and docstrings
- Follow REST API design principles
- Optimize database queries (use select_related/prefetch_related)

### Frontend (React)
- Use functional components with hooks
- Extract custom hooks for reusable logic
- Write comprehensive tests with React Testing Library
- Implement proper error boundaries
- Use consistent prop validation
- Follow Material-UI design patterns
- Optimize performance with memo and useCallback where appropriate

## Testing Requirements

### Backend Testing
- Write unit tests for all models, views, and utilities
- Include integration tests for API endpoints
- Test edge cases and error scenarios
- Maintain high test coverage (>90%)
- Use proper mocking for external dependencies

### Frontend Testing
- Test component rendering and user interactions
- Mock API calls consistently
- Test accessibility features
- Include edge cases and error states
- Test responsive design behavior

## Architecture Patterns

### File Organization
- Group related functionality together
- Use clear, descriptive file names
- Maintain consistent directory structure
- Separate concerns (components, hooks, utilities)

### Component Design
- Keep components focused and single-purpose
- Extract reusable logic into custom hooks
- Use composition over inheritance
- Implement consistent prop interfaces

## Code Review Focus Areas
When suggesting improvements, prioritize:
1. Code duplication elimination
2. Component/function complexity reduction
3. Consistent error handling
4. Performance optimizations
5. Test coverage improvements
6. Documentation quality

## Specific Patterns to Follow
- Use TypeScript/PropTypes for type safety
- Implement consistent API response handling
- Use standardized error message formats
- Follow established naming conventions
- Maintain consistent code formatting
