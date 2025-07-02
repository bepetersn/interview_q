import React from 'react';
import { Modal, Box, IconButton, Paper } from '@mui/material';
import CloseIcon from '@mui/icons-material/Close';
import PropTypes from 'prop-types';
import QuestionLogList from './QuestionLogList.jsx';
import './QuestionLogsModal.css';

function QuestionLogsModal({ open, onClose, question }) {
  return (
    <Modal open={open} onClose={onClose}>
      <Paper className="question-logs-modal-paper">
        {/* Header with close button */}
        <Box className="question-logs-modal-header">
          <IconButton onClick={onClose} aria-label="close">
            <CloseIcon />
          </IconButton>
        </Box>

        {/* Scrollable content area */}
        <div className="question-logs-modal-content">
          {open && (
            <div className="question-logs-modal-inner">
              <QuestionLogList
                questionId={question?.id}
                embedded
                question={question}
                onClose={onClose}
              />
            </div>
          )}
        </div>
      </Paper>
    </Modal>
  );
}

QuestionLogsModal.propTypes = {
  open: PropTypes.bool.isRequired,
  onClose: PropTypes.func.isRequired,
  question: PropTypes.object,
};

export default QuestionLogsModal;
