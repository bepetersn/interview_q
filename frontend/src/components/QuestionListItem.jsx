import React from 'react';
import { ListItem, ListItemText, IconButton, Chip, Box } from '@mui/material';
import { Edit, Delete, ListAlt } from '@mui/icons-material';

function QuestionListItem({ question, onEdit, onDelete, onViewLogs }) {
  return (
    <ListItem key={question.id} alignItems="flex-start" secondaryAction={
      <Box>
        <IconButton edge="end" onClick={() => onEdit(question)}><Edit /></IconButton>
        <IconButton edge="end" onClick={() => onDelete(question.id)}><Delete /></IconButton>
        <IconButton edge="end" onClick={() => onViewLogs(question.id)} title="View Attempts"><ListAlt /></IconButton>
      </Box>
    }>
      <ListItemText
        primary={<Box>
          <b>{question.title}</b> <Chip label={question.difficulty} size="small" sx={{ ml: 1 }} />
        </Box>}
        secondary={
          <>
            <span>{question.notes}</span><br/>
            <span>
              Tags:&nbsp;
              {question.topic_tags && question.topic_tags.map(t => (
                <Chip key={t.id || t} label={t.name || t} size="small" sx={{ mr: 0.5 }} component="span" />
              ))}
            </span><br/>
            <span>Status: {question.is_active ? 'Active' : 'Inactive'}</span>
          </>
        }
        slotProps={{ secondary: { component: 'div' } }}
      />
    </ListItem>
  );
}

export default QuestionListItem;
