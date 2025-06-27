import React from 'react';
import { ListItem, ListItemText, IconButton, Chip, Box, Paper } from '@mui/material';
import { Edit, Delete, ListAlt } from '@mui/icons-material';
import PropTypes from 'prop-types';

function QuestionListItem({ question, onEdit, onDelete, onViewLogs }) {
  return (
    <Paper elevation={3} sx={{ mb: 2, p: 2, background: '#f8fafc', borderRadius: 2, boxShadow: '0 2px 12px rgba(0,0,0,0.08)' }}>
      <ListItem key={question.id} alignItems="flex-start" disableGutters secondaryAction={
        <Box>
          <IconButton edge="end" onClick={() => onEdit(question)}><Edit /></IconButton>
          <IconButton edge="end" onClick={() => onDelete(question.id)}><Delete /></IconButton>
          <IconButton edge="end" onClick={() => onViewLogs(question.id)} title="View Attempts"><ListAlt /></IconButton>
        </Box>
      }>
        <ListItemText
          primary={<Box>
            <span
              role="link"
              aria-label={`View logs for ${question.title}`}
              tabIndex={0}
              style={{ cursor: 'pointer', fontWeight: 700, outline: 'none' }}
              onClick={() => onViewLogs(question.id)}
              onKeyDown={e => { if (e.key === 'Enter' || e.key === ' ') onViewLogs(question.id); }}
              className="question-title-link"
            >
              {question.title}
            </span> <Chip label={question.difficulty} size="small" sx={{ ml: 1 }} onClick={() => {}} />
          </Box>}
          secondary={
            <>
              <span>{question.notes}</span><br/>
              <span>
                Tags:&nbsp;
                {question.tags && question.tags.map(t => (
                  <Chip key={t.id || t} label={t.name || t} size="small" sx={{ mr: 0.5 }} component="span" onClick={() => {}} />
                ))}
              </span><br/>
            </>
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
    notes: PropTypes.string,
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
  }).isRequired,
  onEdit: PropTypes.func.isRequired,
  onDelete: PropTypes.func.isRequired,
  onViewLogs: PropTypes.func.isRequired,
};

export default QuestionListItem;

/* Add hover underline style */
// In your global CSS (e.g., App.css or index.css):
// .question-title-link:hover, .question-title-link:focus { text-decoration: underline; }
