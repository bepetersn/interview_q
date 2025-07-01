import React from 'react';
import PropTypes from 'prop-types';
import {
  Typography,
  List,
  CircularProgress,
  Box
} from '@mui/material';
import QuestionListItem from './QuestionListItem.jsx';

function QuestionsDisplaySection({
  questions,
  loading,
  onEdit,
  onDelete,
  onViewLogs
}) {
  const renderQuestionsList = () => {
    if (loading) {
      return <CircularProgress />;
    }
    if (questions.length === 0) {
      return (
        <Typography variant="body1" color="text.secondary" sx={{ mt: 2 }}>
          No questions found. Click "Add Question" to create your first one.
        </Typography>
      );
    }
    return (
      <List>
        {questions.map((q) => (
          <QuestionListItem
            key={q.id}
            question={q}
            onEdit={onEdit}
            onDelete={onDelete}
            onViewLogs={onViewLogs}
          />
        ))}
      </List>
    );
  };

  return (
    <Box
      sx={{
        width: { xs: '100%', sm: '50vw' },
        maxWidth: { xs: '100%', sm: '50vw' },
        ml: 1,
        boxSizing: 'border-box',
      }}
    >
      {renderQuestionsList()}
    </Box>
  );
}

QuestionsDisplaySection.propTypes = {
  questions: PropTypes.array.isRequired,
  loading: PropTypes.bool.isRequired,
  onEdit: PropTypes.func.isRequired,
  onDelete: PropTypes.func.isRequired,
  onViewLogs: PropTypes.func.isRequired,
};

export default QuestionsDisplaySection;
