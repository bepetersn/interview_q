import React from 'react';
import PropTypes from 'prop-types';
import { Typography, Chip, Box } from '@mui/material';
import './QuestionHeader.css';

function QuestionHeader({ question }) {
  if (!question) return null;

  return (
    <Box className="question-header-container">
      <Box className="question-header-title-row">
        <Typography variant="h4" className="question-header-title">
          {question.title}
        </Typography>
        <Box className="question-header-actions">
          {question.source && (
            <Chip
              label={question.source}
              size="small"
              className="question-header-source-chip"
              sx={{
                backgroundColor: '#e3f2fd',
                color: '#1976d2',
                marginRight: 1,
                '&:hover': {
                  backgroundColor: '#bbdefb',
                  color: '#0d47a1'
                }
              }}
            />
          )}
          {question.difficulty && (
            <Chip
              label={question.difficulty}
              size="small"
              className="question-header-difficulty-chip"
              sx={{
                backgroundColor: '#e0e0e0',
                color: 'rgba(0, 0, 0, 0.6)',
                '&:hover': {
                  backgroundColor: '#c8e6c9',
                  color: '#1b5e20'
                }
              }}
            />
          )}
        </Box>
      </Box>

      {question.tags && question.tags.length > 0 && (
        <Box className="question-header-tags-container">
          <Typography variant="body2" component="span" color="text.secondary">
            Tags:&nbsp;
          </Typography>
          {question.tags.map(tag => (
            <Chip
              key={tag.id}
              label={tag.name}
              size="small"
              className="question-header-tag-chip"
              component="span"
              sx={{
                backgroundColor: '#f0f0f0 !important',
                color: 'rgba(0, 0, 0, 0.6) !important',
                border: '1px solid #d0d0d0 !important',
                '&:hover': {
                  backgroundColor: '#d0d0d0 !important',
                  color: 'rgba(0, 0, 0, 0.87) !important'
                }
              }}
            />
          ))}
        </Box>
      )}
    </Box>
  );
}

QuestionHeader.propTypes = {
  question: PropTypes.object,
};

export default QuestionHeader;
