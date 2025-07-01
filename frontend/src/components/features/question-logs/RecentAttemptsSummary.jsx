import React from 'react';
import PropTypes from 'prop-types';
import { Typography, Chip, Box } from '@mui/material';

function RecentAttemptsSummary({ logs }) {
  const getOutcomeColor = (outcome) => {
    switch (outcome) {
      case 'Solved': return 'success.light';
      case 'Partial': return 'warning.light';
      case 'Failed': return 'error.light';
      default: return 'grey.300';
    }
  };

  const getOutcomeTextColor = (outcome) => {
    switch (outcome) {
      case 'Solved': return 'success.contrastText';
      case 'Partial': return 'warning.contrastText';
      case 'Failed': return 'error.contrastText';
      default: return 'text.secondary';
    }
  };

  if (!logs || logs.length === 0) return null;

  return (
    <Box sx={{
      mb: 2,
      p: 1.5,
      backgroundColor: 'grey.50',
      borderRadius: 1,
      border: '1px solid',
      borderColor: 'grey.200'
    }}>
      <Typography variant="subtitle2" sx={{ fontWeight: 600, mb: 1, color: 'text.primary' }}>
        Recent Attempts ({logs.length})
      </Typography>
      {logs.slice(0, 3).map((log, index) => (
        <Box key={log.id} sx={{ display: 'flex', alignItems: 'center', gap: 1, mb: index < 2 ? 0.5 : 0 }}>
          <Typography variant="caption" color="text.secondary" sx={{ minWidth: '70px' }}>
            {new Date(log.date_attempted).toLocaleDateString()}
          </Typography>
          <Chip
            label={log.outcome || 'No outcome'}
            size="small"
            sx={{
              fontSize: '0.65rem',
              height: '20px',
              backgroundColor: getOutcomeColor(log.outcome),
              color: getOutcomeTextColor(log.outcome)
            }}
          />
          <Typography variant="caption" color="text.secondary">
            {log.time_spent_min}min
          </Typography>
          {log.solution_approach && (
            <Typography variant="caption" color="text.secondary" sx={{
              overflow: 'hidden',
              textOverflow: 'ellipsis',
              whiteSpace: 'nowrap',
              maxWidth: '150px'
            }}>
              • {log.solution_approach}
            </Typography>
          )}
        </Box>
      ))}
    </Box>
  );
}

RecentAttemptsSummary.propTypes = {
  logs: PropTypes.array.isRequired,
};

export default RecentAttemptsSummary;
