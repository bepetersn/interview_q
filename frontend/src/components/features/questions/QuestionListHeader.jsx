import React from 'react';
import PropTypes from 'prop-types';
import {
  Typography,
  Button,
  Box
} from '@mui/material';
import { Add } from '@mui/icons-material';

function QuestionListHeader({ onAddQuestion, onManageTags, error }) {
  return (
    <>
      <Box display="flex" flexDirection="column" alignItems="flex-start" mb={2}>
        <Typography variant="h4" gutterBottom sx={{ mb: 1, ml: 1 }}>
          Questions
        </Typography>
        <Button
          variant="outlined"
          startIcon={<Add />}
          onClick={onAddQuestion}
          sx={{ mb: 1, ml: 1 }}
        >
          Add Question
        </Button>
      </Box>
      <Button
        variant="text"
        onClick={onManageTags}
        sx={{ mb: 2, ml: 1 }}
      >
        Manage Tags
      </Button>
      {error && (
        <Typography color="error" sx={{ mb: 2, ml: 1 }}>
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
