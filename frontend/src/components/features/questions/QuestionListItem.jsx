import React from 'react';
import { ListItem, ListItemText, IconButton, Chip, Box, Paper } from '@mui/material';
import { Delete } from '@mui/icons-material';
import PropTypes from 'prop-types';
import './QuestionListItem.css';


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


const formatLastAttempted = (lastAttempted) => {
  return lastAttempted ? new Date(lastAttempted).toLocaleDateString() : 'Never';
};

// Sub-components

const QuestionActions = ({ questionId, onDelete }) => (
  <Box className="question-actions">
    <IconButton
      edge="end"
      onClick={(e) => {
        e.stopPropagation();
        onDelete(questionId);
      }}
      title="Delete Question"
      size="small"
    >
      <Delete />
    </IconButton>
  </Box>
);

const QuestionHeader = ({ question }) => (
  <Box className="question-header">
    <span className="question-title">{question.title}</span>
    {question.source && (
      <Chip
        label={question.source}
        size="small"
        className="source-chip"
        onClick={(e) => e.stopPropagation()}
        sx={{
          backgroundColor: '#e3f2fd',
          color: '#1976d2',
          fontSize: '0.7rem',
          '&:hover': {
            backgroundColor: '#bbdefb',
            color: '#0d47a1'
          }
        }}
      />
    )}
    <Chip
      label={question.difficulty}
      size="small"
      className={`difficulty-chip ${getDifficultyClass(question.difficulty)}`}
      onClick={(e) => e.stopPropagation()}
    />
  </Box>
);

const QuestionTags = ({ tags }) => (
  <Box className="question-tags">
    <span className="tags-label">Tags:</span>
    {tags?.map(tag => (
      <Chip
        key={tag.id}
        label={tag.name}
        size="small"
        className="tag-chip"
        component="span"
        onClick={(e) => e.stopPropagation()}
      />
    ))}
  </Box>
);

const QuestionInfo = ({ question }) => (
  <Box className="question-info">
    <QuestionTags tags={question.tags} />
    <span className="question-metadata">
      Attempts: {question.attempts_count || 0}, Last: {formatLastAttempted(question.last_attempted_at)}
    </span>
  </Box>
);

function QuestionListItem({ question, onDelete, onViewLogs }) {
  const handleItemClick = () => {
    onViewLogs(question.id);
  };

  return (
    <Paper elevation={4} className="question-card" onClick={handleItemClick} style={{ cursor: 'pointer' }}>
      <ListItem
        alignItems="flex-start"
        disableGutters
        secondaryAction={<QuestionActions questionId={question.id} onDelete={onDelete} />}
        className="question-list-item"
      >
        <ListItemText
          primary={<QuestionHeader question={question} />}
          secondary={<QuestionInfo question={question} />}
          slotProps={{ secondary: { component: 'div' } }}
        />
      </ListItem>
    </Paper>
  );
}


// PropTypes for sub-components
QuestionActions.propTypes = {
  questionId: PropTypes.oneOfType([PropTypes.string, PropTypes.number]).isRequired,
  onDelete: PropTypes.func.isRequired,
};

QuestionHeader.propTypes = {
  question: PropTypes.shape({
    id: PropTypes.oneOfType([PropTypes.string, PropTypes.number]).isRequired,
    title: PropTypes.string.isRequired,
    difficulty: PropTypes.string,
    source: PropTypes.string,
  }).isRequired,
};

QuestionTags.propTypes = {
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
};

QuestionInfo.propTypes = {
  question: PropTypes.shape({
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
    last_attempted_at: PropTypes.string,
    attempts_count: PropTypes.number,
  }).isRequired,
};

QuestionListItem.propTypes = {
  question: PropTypes.shape({
    id: PropTypes.oneOfType([PropTypes.string, PropTypes.number]).isRequired,
    title: PropTypes.string.isRequired,
    difficulty: PropTypes.string,
    content: PropTypes.string,
    source: PropTypes.string,
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
