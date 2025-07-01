import React from 'react';
import { Drawer, Box, IconButton } from '@mui/material';
import CloseIcon from '@mui/icons-material/Close';
import PropTypes from 'prop-types';
import QuestionLogList from './QuestionLogList.jsx';

function QuestionLogsDrawer({ open, onClose, question }) {
  return (
    <Drawer anchor="right" open={open} onClose={onClose}>
      <Box sx={{ width: { xs: '100vw', sm: 480 }, p: 2 }}>
        <Box display="flex" justifyContent="flex-end">
          <IconButton onClick={onClose} aria-label="close">
            <CloseIcon />
          </IconButton>
        </Box>
        {open && (
          <QuestionLogList questionId={question?.id} embedded question={question} onClose={onClose} />
        )}
      </Box>
    </Drawer>
  );
}

QuestionLogsDrawer.propTypes = {
  open: PropTypes.bool.isRequired,
  onClose: PropTypes.func.isRequired,
  question: PropTypes.object,
};

export default QuestionLogsDrawer;
