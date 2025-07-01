# Question Logs Components

This directory contains the refactored Question Logs components that were broken down from the original monolithic `QuestionLogList` component.

## Components

### QuestionLogList.jsx (Main Component)
The main container component that orchestrates all the smaller components. It handles navigation, state management via the custom hook, and renders all child components.

**Props:**
- `questionId` - ID of the question
- `embedded` - Boolean to indicate if used in embedded mode (drawer)
- `question` - Question object (for embedded usage)
- `onClose` - Callback function for closing

### QuestionHeader.jsx
Displays question information including title, difficulty, tags, and content.

**Props:**
- `question` - Question object containing title, difficulty, tags, and content

### RecentAttemptsSummary.jsx
Shows a summary box of the most recent attempts (up to 3) with date, outcome, time spent, and solution approach.

**Props:**
- `logs` - Array of log objects

### LogForm.jsx
Dialog component for creating and editing logs. Handles all form state internally and communicates with parent via callbacks.

**Props:**
- `open` - Boolean to control dialog visibility
- `onClose` - Callback when dialog should close
- `onSave` - Callback when save is triggered, receives form data
- `editLog` - Log object when editing (null for new logs)
- `questionId` - ID of the question
- `questionTitle` - Title of the question for display
- `error` - Error message to display
- `saving` - Boolean indicating save operation in progress

### LogList.jsx
Placeholder component for future log list/table functionality. Currently returns null as the original component only showed recent attempts in the summary.

**Props:**
- `logs` - Array of log objects

### useQuestionLogs.js (Custom Hook)
Custom hook that handles all data fetching and API operations for question logs.

**Parameters:**
- `questionId` - ID of the question
- `questionProp` - Question object (optional, for embedded usage)

**Returns:**
- `logs` - Array of logs
- `question` - Question object
- `error` - Error message string
- `setError` - Function to set error message
- `saveLog` - Function to save a log (create or update)
- `fetchLogs` - Function to refetch logs

## Benefits of Refactoring

1. **Separation of Concerns**: Each component has a single responsibility
2. **Reusability**: Components can be reused in other parts of the application
3. **Testability**: Smaller components are easier to test in isolation
4. **Maintainability**: Changes to specific functionality are contained within relevant components
5. **Custom Hook**: Data fetching logic is extracted and can be reused
6. **Cleaner Code**: The main component is much more readable and focused

## Usage

```jsx
import { QuestionLogList } from './components/features/question-logs';

// Standalone usage
<QuestionLogList />

// Embedded usage (in drawer)
<QuestionLogList
  questionId="123"
  embedded={true}
  question={questionObject}
  onClose={handleClose}
/>
```

You can also import individual components if needed:

```jsx
import {
  QuestionHeader,
  RecentAttemptsSummary,
  LogForm,
  useQuestionLogs
} from './components/features/question-logs';
```
