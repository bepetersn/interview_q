import React from 'react';
import { ListItem, ListItemText, IconButton, Chip, Box, Paper } from '@mui/material';
import { Delete, ListAlt } from '@mui/icons-material';
import PropTypes from 'prop-types';
import './QuestionListItem.css';

function QuestionListItem({ question, onDelete, onViewLogs }) {
  const getDifficultyClass = (difficulty) => {
    switch (difficulty?.toLowerCase()) {
      case 'easy':
        return 'easy';
      case 'medium':
        return 'medium';
      case 'hard':
        return 'hard';
      default:
        return '';
    }
  };

  return (
    <Paper elevation={3} sx={{ mb: 2, p: 1.5, background: '#ffffff', borderRadius: 2, boxShadow: '0 2px 12px rgba(0,0,0,0.15)' }}>
      <ListItem key={question.id} alignItems="flex-start" disableGutters secondaryAction={
        <Box>
          <IconButton edge="end" onClick={() => onViewLogs(question.id)} title="View Attempts"><ListAlt /></IconButton>
          <IconButton edge="end" onClick={() => onDelete(question.id)} title="Delete Question"><Delete /></IconButton>
        </Box>
      }>
        <ListItemText
          primary={
            <Box display="flex" alignItems="center">
              <button className="question-title-button" onClick={() => onViewLogs(question.id)}>
                {question.title}
              </button>
              <Chip label={question.difficulty} size="small" className={`difficulty-chip ${getDifficultyClass(question.difficulty)}`} sx={{ ml: 1 }} />
            </Box>}
          secondary={
            <Box mt={1}>
              <span>
                Tags:&nbsp;
                {question.tags && question.tags.map(tag => (
                  <Chip
                    key={tag.id}
                    label={tag.name}
                    size="small"
                    className="tag-chip"
                    component="span"
                  />
                ))}
              </span>
              <span style={{ marginLeft: '8px' }}>
                Attempts: {question.attempts_count || 0}, Last: {question.last_attempted_at ? new Date(question.last_attempted_at).toLocaleDateString() : 'Never'}
              </span>
            </Box>
          }
          slotProps={{ secondary: { component: 'div' } }}
        />
      </ListItem>
    </Paper>
  );
}

QuestionListItem.propTypes = {
  question: PropTypes.shape({
    id: PropTypes.oneOfType([PropTypes.string, PropTypes.number]).isRequired,
    title: PropTypes.string.isRequired,
    difficulty: PropTypes.string,
    content: PropTypes.string,
    tags: PropTypes.arrayOf(
      PropTypes.oneOfType([
        PropTypes.shape({
          id: PropTypes.oneOfType([PropTypes.string, PropTypes.number]),
          name: PropTypes.string,
        }),
        PropTypes.string,
        PropTypes.number,
      ])
    ),
    is_active: PropTypes.bool,
    last_attempted_at: PropTypes.string,
    attempts_count: PropTypes.number,
  }).isRequired,
  onDelete: PropTypes.func.isRequired,
  onViewLogs: PropTypes.func.isRequired,
};

export default QuestionListItem;
