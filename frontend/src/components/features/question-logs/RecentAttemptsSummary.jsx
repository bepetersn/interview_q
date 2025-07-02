import React from 'react';
import PropTypes from 'prop-types';
import { Typography, Chip } from '@mui/material';
import './RecentAttemptsSummary.css';

function RecentAttemptItem({ log }) {
  const getOutcomeChipClass = (outcome) => {
    const baseClass = 'recent-attempts-chip';
    switch (outcome) {
      case 'Solved': return `${baseClass} recent-attempts-chip-solved`;
      case 'Partial': return `${baseClass} recent-attempts-chip-partial`;
      case 'Failed': return `${baseClass} recent-attempts-chip-failed`;
      default: return `${baseClass} recent-attempts-chip-default`;
    }
  };

  return (
    <div key={log.id} className="recent-attempts-item">
      <Typography variant="caption" className="recent-attempts-date">
        {new Date(log.date_attempted).toLocaleDateString()}
      </Typography>
      <Chip
        label={log.outcome || 'No outcome'}
        size="small"
        className={getOutcomeChipClass(log.outcome)}
      />
      <Typography variant="caption" className="recent-attempts-time">
        {log.time_spent_min}min
      </Typography>
      {log.solution_approach && (
        <Typography variant="caption" className="recent-attempts-approach">
          • {log.solution_approach}
        </Typography>
      )}
    </div>
  );
}

RecentAttemptItem.propTypes = {
  log: PropTypes.object.isRequired,
};

function RecentAttemptsSummary({ logs }) {
  if (!logs || logs.length === 0) {
    return (
      <Typography variant="body1" className="recent-attempts-empty">
        No attempts have been made yet.
      </Typography>
    );
  }

  return (
    <div className="recent-attempts-container">
      <Typography variant="subtitle2" className="recent-attempts-title">
        Recent Attempts ({logs.length})
      </Typography>
      {logs.slice(0, 3).map((log) => (
        <RecentAttemptItem key={log.id} log={log} />
      ))}
    </div>
  );
}

RecentAttemptsSummary.propTypes = {
  logs: PropTypes.array.isRequired,
};

export default RecentAttemptsSummary;
