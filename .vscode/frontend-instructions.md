# Frontend Development Instructions

## Component Standards

### File Organization
```
src/
├── components/
│   ├── common/          # Reusable UI components
│   ├── features/        # Feature-specific components
│   └── pages/           # Page-level components
├── hooks/               # Custom hooks
├── utils/               # Utility functions
├── services/            # API service layer
└── __tests__/           # Test files
```

### Component Template
```javascript
import React, { memo } from 'react';
import PropTypes from 'prop-types';

/**
 * Brief description of component purpose
 * @param {Object} props - Component props
 * @param {string} props.title - Title to display
 */
const ComponentName = memo(({ title, onAction }) => {
  // Component logic here

  return (
    <div>
      {/* Component JSX */}
    </div>
  );
});

ComponentName.propTypes = {
  title: PropTypes.string.isRequired,
  onAction: PropTypes.func,
};

ComponentName.defaultProps = {
  onAction: () => {},
};

export default ComponentName;
```

### Testing Template
```javascript
import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import { vi } from 'vitest';
import ComponentName from '../ComponentName';

describe('ComponentName', () => {
  it('renders correctly', () => {
    render(<ComponentName title="Test" />);
    expect(screen.getByText('Test')).toBeInTheDocument();
  });

  it('handles user interactions', () => {
    const mockAction = vi.fn();
    render(<ComponentName title="Test" onAction={mockAction} />);

    fireEvent.click(screen.getByRole('button'));
    expect(mockAction).toHaveBeenCalledTimes(1);
  });
});
```

## API Integration Standards

### Service Layer Pattern
```javascript
// services/api.js
import axios from 'axios';

const api = axios.create({
  baseURL: process.env.REACT_APP_API_URL,
});

export const questionService = {
  getAll: () => api.get('/questions/'),
  getById: (id) => api.get(`/questions/${id}/`),
  create: (data) => api.post('/questions/', data),
  update: (id, data) => api.put(`/questions/${id}/`, data),
  delete: (id) => api.delete(`/questions/${id}/`),
};
```

### Custom Hook Pattern
```javascript
// hooks/useQuestions.js
import { useState, useEffect } from 'react';
import { questionService } from '../services/api';

export const useQuestions = () => {
  const [questions, setQuestions] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchQuestions = async () => {
      try {
        const response = await questionService.getAll();
        setQuestions(response.data);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchQuestions();
  }, []);

  return { questions, loading, error };
};
```

## Testing Requirements

### What to Test
- Component rendering with different props
- User interactions (clicks, form submissions)
- API integration (mocked)
- Error handling scenarios
- Accessibility features
- Edge cases (empty states, loading states)

### Testing Utilities
```javascript
// test-utils.js
import React from 'react';
import { render } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import { ThemeProvider } from '@mui/material/styles';
import theme from '../theme';

export const renderWithProviders = (ui, options = {}) => {
  const Wrapper = ({ children }) => (
    <BrowserRouter>
      <ThemeProvider theme={theme}>
        {children}
      </ThemeProvider>
    </BrowserRouter>
  );

  return render(ui, { wrapper: Wrapper, ...options });
};
```

## Common Patterns to Follow

### Error Handling
```javascript
const handleSubmit = async (data) => {
  try {
    setLoading(true);
    await questionService.create(data);
    onSuccess();
  } catch (error) {
    setError(error.response?.data?.message || 'An error occurred');
  } finally {
    setLoading(false);
  }
};
```

### Loading States
```javascript
if (loading) return <CircularProgress />;
if (error) return <Alert severity="error">{error}</Alert>;
if (!data.length) return <EmptyState />;
```

### Form Validation
```javascript
const validateForm = (data) => {
  const errors = {};

  if (!data.title) errors.title = 'Title is required';
  if (!data.content) errors.content = 'Content is required';

  return errors;
};
```

## Performance Optimization

### Use React.memo for expensive components
### Use useCallback for event handlers passed to children
### Use useMemo for expensive calculations
### Implement proper key props for lists
### Lazy load components when appropriate

## Accessibility Standards

### Always include proper ARIA labels
### Ensure keyboard navigation works
### Use semantic HTML elements
### Include alt text for images
### Test with screen readers
