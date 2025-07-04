# AI Code Review Instructions

## Automatic Code Review Checklist

When reviewing code, always check for:

### 🔍 **Code Quality**
- [ ] Single Responsibility Principle - each function/component has one clear purpose
- [ ] DRY violations - identify duplicated code that can be extracted
- [ ] Meaningful variable and function names
- [ ] Proper error handling and validation
- [ ] Consistent code formatting and style

### 🧪 **Testing**
- [ ] Missing test cases for new functionality
- [ ] Edge cases and error scenarios covered
- [ ] Proper mocking of external dependencies
- [ ] Test names clearly describe what they test
- [ ] Integration tests for complex workflows

### 🏗️ **Architecture**
- [ ] Proper separation of concerns
- [ ] Components/functions are not too large or complex
- [ ] Consistent patterns used across similar code
- [ ] Proper abstraction levels
- [ ] Clear dependency flow

### 📚 **Documentation**
- [ ] Public functions have docstrings
- [ ] Complex business logic is commented
- [ ] README updated if needed
- [ ] API documentation reflects changes

### ⚡ **Performance**
- [ ] No unnecessary re-renders (React)
- [ ] Efficient database queries (Django)
- [ ] Proper use of caching where applicable
- [ ] Memory leaks prevented

### 🔐 **Security**
- [ ] Input validation implemented
- [ ] Proper authentication/authorization
- [ ] No sensitive data exposed
- [ ] SQL injection prevention

## Review Response Format

When providing code review feedback, use this format:

```markdown
## 🔧 **Critical Issues** (Must Fix)
- Issue description with file:line reference
- Specific recommendation
- Code example if helpful

## ⚠️ **Suggestions** (Should Consider)
- Improvement opportunity
- Explanation of benefit
- Alternative approach

## ✅ **Positive Notes**
- Good practices observed
- Well-implemented features

## 📋 **Refactoring Opportunities**
- Code that could be simplified
- Extraction opportunities
- Consistency improvements
```

## Common Anti-Patterns to Flag

### Backend (Django)
```python
# ❌ Bad - N+1 queries
def get_questions_with_tags():
    questions = Question.objects.all()
    for question in questions:
        tags = question.tags.all()  # N+1 query problem

# ✅ Good - Optimized query
def get_questions_with_tags():
    return Question.objects.prefetch_related('tags').all()
```

### Frontend (React)
```javascript
// ❌ Bad - Component doing too much
const QuestionPage = () => {
  const [questions, setQuestions] = useState([]);
  const [loading, setLoading] = useState(true);
  const [tags, setTags] = useState([]);
  const [selectedTag, setSelectedTag] = useState('');

  // 50+ lines of logic mixing API calls, filtering, UI state...
};

// ✅ Good - Separated concerns
const QuestionPage = () => {
  const { questions, loading } = useQuestions();
  const { tags } = useTags();
  const { filteredQuestions } = useQuestionFiltering(questions, selectedTag);

  return <QuestionList questions={filteredQuestions} />;
};
```

## Code Complexity Guidelines

### Function/Component Size Limits
- **Functions**: Ideally under 20 lines, max 50 lines
- **React Components**: Ideally under 100 lines, max 200 lines
- **Django Views**: Ideally under 30 lines, max 100 lines

### Complexity Indicators
- More than 3 nested if statements (can be flexible)
- Functions with more than 3 parameters (besides self)
- Components with more than 10 state variables
- Files with more than 250 lines

## Refactoring Suggestions

### When to Extract
- Logic used in multiple places
- Complex conditional logic
- Long parameter lists
- Mixed abstraction levels

### How to Extract
```python
# Extract complex logic
def calculate_question_difficulty_score(question):
    """Calculate difficulty score based on multiple factors."""
    base_score = DIFFICULTY_SCORES[question.difficulty]
    tag_bonus = len(question.tags.all()) * 0.1
    completion_penalty = question.completion_rate * 0.2
    return base_score + tag_bonus - completion_penalty

# Extract validation logic
def validate_question_data(data):
    """Validate question data before saving."""
    errors = {}
    if not data.get('title'):
        errors['title'] = 'Title is required'
    if len(data.get('content', '')) < 10:
        errors['content'] = 'Content must be at least 10 characters'
    return errors
```

## Testing Coverage Requirements

### Backend Testing
- Models: 100% coverage
- Views: 95% coverage
- Serializers: 90% coverage
- Utility functions: 100% coverage

### Frontend Testing
- Components: 85% coverage
- Hooks: 90% coverage
- Utilities: 95% coverage
- Integration flows: 80% coverage

## Performance Benchmarks

### Backend
- API response time < 200ms for simple queries
- Database queries < 50ms
- Memory usage growth < 10MB per request

### Frontend
- Initial page load < 3 seconds
- Component re-render time < 100ms
- Bundle size < 1MB compressed

## Review Automation

### Automated Checks
- Code formatting (Black, Prettier)
- Import organization
- Unused imports/variables
- Basic security scanning
- Test coverage reporting

### Manual Review Focus
- Business logic correctness
- Architecture decisions
- User experience implications
- Performance considerations
- Security vulnerabilities
