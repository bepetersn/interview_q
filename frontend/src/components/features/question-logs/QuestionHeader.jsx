import React from 'react';
import PropTypes from 'prop-types';
import { Typography, Chip, Box } from '@mui/material';

const styles = {
  difficultyChip: {
    ml: 1,
    backgroundColor: 'primary.main',
    color: 'white',
    fontWeight: 'bold',
    '& .MuiChip-label': {
      fontSize: '0.75rem',
    },
    '&:hover': {
      backgroundColor: 'primary.dark',
    },
  },
  tagChip: {
    mr: 0.5,
    backgroundColor: 'secondary.light',
    color: 'secondary.contrastText',
    border: '1px solid',
    borderColor: 'secondary.main',
    '& .MuiChip-label': {
      fontSize: '0.7rem',
    },
    '&:hover': {
      backgroundColor: 'secondary.main',
      color: 'white',
    },
  },
};

function QuestionHeader({ question }) {
  if (!question) return null;

  return (
    <Box sx={{ textAlign: 'left', mb: 2 }}>
      <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
        <Typography variant="h6" sx={{ fontWeight: 700 }}>
          {question.title}
        </Typography>
        {question.difficulty && (
          <Chip label={question.difficulty} size="small" sx={styles.difficultyChip} />
        )}
      </Box>

      {question.tags && question.tags.length > 0 && (
        <Box sx={{ mb: 2 }}>
          <Typography variant="body2" component="span" color="text.secondary">
            Tags:&nbsp;
          </Typography>
          {question.tags.map(tag => (
            <Chip
              key={tag.id}
              label={tag.name}
              size="small"
              sx={styles.tagChip}
              component="span"
            />
          ))}
        </Box>
      )}

      {question.content && (
        <Typography
          variant="body2"
          color="text.secondary"
          sx={{ mb: 2 }}
          dangerouslySetInnerHTML={{ __html: question.content }}
        />
      )}
    </Box>
  );
}

QuestionHeader.propTypes = {
  question: PropTypes.object,
};

export default QuestionHeader;
