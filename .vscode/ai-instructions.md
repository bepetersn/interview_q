# VSCode AI Assistant Instructions

## Project Context
Interview Questions App - Django REST Framework backend with React frontend for managing programming interview questions and activity logs.

## Development Priorities
1. **Code Quality**: Maintain high standards for readability, maintainability, and consistency
2. **Testing**: Comprehensive test coverage, especially for frontend components
3. **Architecture**: Clean separation of concerns and consistent patterns
4. **Performance**: Optimize both backend queries and frontend rendering

## Code Style Guidelines

### Python/Django
```python
# Preferred patterns:
class QuestionViewSet(viewsets.ModelViewSet):
    """ViewSet for managing interview questions."""

    def get_queryset(self):
        return Question.objects.select_related('category').prefetch_related('tags')
```

### React/JavaScript
```javascript
// Preferred patterns:
const QuestionList = ({ onQuestionSelect }) => {
  const { questions, loading, error } = useQuestions();

  if (loading) return <LoadingSpinner />;
  if (error) return <ErrorMessage error={error} />;

  return (
    <List>
      {questions.map(question => (
        <QuestionItem key={question.id} question={question} />
      ))}
    </List>
  );
};
```

## Testing Standards

### Backend Tests
- Use pytest with Django fixtures
- Mock external API calls
- Test both success and failure scenarios
- Include integration tests for complete workflows

### Frontend Tests
- Use React Testing Library
- Mock API calls with consistent patterns
- Test user interactions and accessibility
- Include edge cases and error states

## Architecture Decisions

### Backend
- Use Django REST Framework ViewSets
- Implement proper serializer validation
- Use custom managers for complex queries
- Maintain clear separation between models, views, and business logic

### Frontend
- Use functional components with hooks
- Extract business logic into custom hooks
- Implement consistent error handling
- Use Material-UI components with custom theming

## Refactoring Guidelines
When suggesting improvements:
1. Identify code duplication and extract reusable components/functions
2. Break down complex components into smaller, focused pieces
3. Improve error handling and user feedback
4. Optimize performance where possible
5. Ensure consistent patterns across similar components

## Common Issues to Address
- Large components doing multiple things
- Inconsistent API error handling
- Missing test coverage for edge cases
- Code duplication across similar components
- Inconsistent naming conventions

## AI Assistant Behavior
- Always suggest comprehensive test cases when creating new components / views / bigger bits of functionality
- Prioritize code quality and maintainability over speed
- Provide refactoring suggestions for complex code
- Suggest architectural improvements when appropriate
- Focus on consistency with existing codebase patterns, except where the current codebase is deficient.
