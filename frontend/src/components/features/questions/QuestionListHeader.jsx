import React from 'react';
import PropTypes from 'prop-types';
import {
  Typography,
  Button,
  Box
} from '@mui/material';
import { Add } from '@mui/icons-material';
import './QuestionListHeader.css';

function QuestionListHeader({ onAddQuestion, onManageTags, error }) {
  return (
    <>
      <Box display="flex" flexDirection="column" alignItems="flex-start" mb={2}>
        <Typography variant="h4" gutterBottom sx={{ mb: 1, ml: 1 }}>
          Questions
        </Typography>
        <Button
          className="add-question-button"
          variant="contained"
          startIcon={<Add />}
          onClick={onAddQuestion}
        >
          Add Question
        </Button>
        <Button
          className="manage-tags-button"
          variant="outlined"
          onClick={onManageTags}
        >
          Manage Tags
        </Button>
      </Box>
      {error && (
        <Typography className="error-message">
          {error}
        </Typography>
      )}
    </>
  );
}

QuestionListHeader.propTypes = {
  onAddQuestion: PropTypes.func.isRequired,
  onManageTags: PropTypes.func.isRequired,
  error: PropTypes.string,
};

export default QuestionListHeader;
