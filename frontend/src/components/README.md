# Component Organization

This directory contains all React components organized by features and pages for better maintainability and code organization.

## Directory Structure

```
components/
├── pages/                     # Main page components (top-level routes)
│   ├── App.jsx               # Main application component
│   ├── QuestionList.jsx      # Questions list page
│   └── index.js              # Page exports
├── features/                  # Feature-specific components
│   ├── auth/                 # Authentication features
│   │   ├── LoginPage.jsx     # Login form and logic
│   │   ├── RegisterPage.jsx  # Registration form and logic
│   │   └── index.js          # Auth feature exports
│   ├── questions/            # Question management features
│   │   ├── QuestionFormDialog.jsx      # Create/edit question form
│   │   ├── QuestionListHeader.jsx      # Header with actions
│   │   ├── QuestionListItem.jsx        # Individual question display
│   │   ├── QuestionsDisplaySection.jsx # Questions list display
│   │   └── index.js                    # Question feature exports
│   ├── tags/                 # Tag management features
│   │   ├── TagList.jsx               # Tag CRUD operations
│   │   ├── TagManagementDialog.jsx   # Tag management modal
│   │   └── index.js                  # Tag feature exports
│   └── question-logs/        # Question logging features
│       ├── QuestionLogList.jsx    # List and manage question attempts
│       ├── QuestionLogsDrawer.jsx # Side drawer for logs
│       └── index.js               # Question logs feature exports
├── common/                   # Shared/reusable components (future)
│   └── index.js              # Common component exports
├── __tests__/               # Component tests
└── index.js                 # Main component exports
```

## Organization Principles

### **Pages** (`pages/`)
- Top-level components that represent entire pages or routes
- These are the components that get rendered for specific routes in React Router
- Should compose features together rather than contain business logic

### **Features** (`features/`)
- Components grouped by business domain/feature
- Each feature directory contains all components related to that functionality
- Features should be as self-contained as possible
- Each feature has an `index.js` for clean exports

### **Common** (`common/`)
- Reusable components that are used across multiple features
- UI components that don't belong to a specific business domain
- Examples: Loading spinners, generic modals, form components, etc.

## Import Patterns

### Recommended Import Style

```jsx
// Import from feature index files for cleaner imports
import { QuestionFormDialog, QuestionListHeader } from '../features/questions/index.js';
import { TagManagementDialog } from '../features/tags/index.js';

// Or import from the main components index
import { QuestionFormDialog, LoginPage } from '../../components/index.js';
```

### Benefits of This Organization

1. **Feature Isolation**: Related components are grouped together
2. **Easy Navigation**: Clear directory structure makes finding components intuitive
3. **Scalability**: Easy to add new features without cluttering the root components directory
4. **Reusability**: Common components can be shared across features
5. **Testing**: Tests can be organized by feature
6. **Bundle Splitting**: Potential for code splitting by feature in the future

## Adding New Components

### For a New Feature
1. Create a new directory under `features/`
2. Add your components to that directory
3. Create an `index.js` file to export the feature's components
4. Update the main `components/index.js` to re-export from your feature

### For Common Components
1. Add components to the `common/` directory
2. Export them from `common/index.js`
3. They'll be available through the main `components/index.js`

### For New Pages
1. Add to the `pages/` directory
2. Export from `pages/index.js`
3. Add the route in `App.jsx`
