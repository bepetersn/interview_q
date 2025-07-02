import React, { useState } from 'react';
import PropTypes from 'prop-types';
import { useParams, useNavigate } from 'react-router-dom';
import { Typography, Box } from '@mui/material';
import { BackButton, NewButton } from '../../common';
import QuestionHeader from './QuestionHeader';
import RecentAttemptsSummary from './RecentAttemptsSummary';
import LogForm from './LogForm';
import LogList from './LogList';
import { useQuestionLogs } from './useQuestionLogs';
import './QuestionLogList.css';

function QuestionLogList({ questionId: propQuestionId, embedded = false, question: questionProp, onClose }) {
  const { questionId: paramQuestionId } = useParams();
  const questionId = propQuestionId || paramQuestionId;
  const navigate = useNavigate();

  const { logs, question, error, setError, saveLog } = useQuestionLogs(questionId, questionProp);

  const [open, setOpen] = useState(false);
  const [saving, setSaving] = useState(false);

  const handleOpen = () => {
    setOpen(true);
  };

  const handleClose = () => {
    setOpen(false);
  };

  const handleSave = async (formData) => {
    setSaving(true);
    setError('');

    const success = await saveLog(formData, null); // Always create new log
    if (success) {
      handleClose();
    }

    setSaving(false);
  };

  const handleBack = () => {
    if (embedded) {
      onClose();
    } else {
      navigate('/');
    }
  };

  return (
    <div className="question-log-list-container">
      <div className="question-log-list-header">
        <QuestionHeader question={question} />
        <NewButton onClick={() => handleOpen()} text="Add Log" className="new-log-button" />
      </div>
      <div className="question-log-list-content">
        <div className="question-log-list-main">
          {question.content && (
            <Box className="question-content-box">
              <Typography
                variant="body2"
                color="text.secondary"
                dangerouslySetInnerHTML={{ __html: question.content }}
              />
            </Box>
          )}
          <LogList logs={logs} />
        </div>
        <RecentAttemptsSummary logs={logs} className="recent-attempts-summary" />
      </div>

      {error && (
        <Typography color="error" className="question-log-list-error">
          {error}
        </Typography>
      )}

      <LogForm
        open={open}
        onClose={handleClose}
        onSave={handleSave}
        questionId={questionId}
        questionTitle={question?.title}
        error={error}
        saving={saving}
      />
    </div>
  );
}

QuestionLogList.propTypes = {
  questionId: PropTypes.string,
  embedded: PropTypes.bool,
  question: PropTypes.object,
  onClose: PropTypes.func,
};

export default QuestionLogList;
