import React, { useState } from 'react';
import PropTypes from 'prop-types';
import { useParams, useNavigate } from 'react-router-dom';
import { Typography } from '@mui/material';
import { BackButton, NewButton } from '../../common';
import QuestionHeader from './QuestionHeader';
import RecentAttemptsSummary from './RecentAttemptsSummary';
import LogForm from './LogForm';
import LogList from './LogList';
import { useQuestionLogs } from './useQuestionLogs';

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

  const questionTitle = question?.title;

  return (
    <div>
      <BackButton
        onClick={handleBack}
        text={embedded ? 'Back' : 'Back to Questions'}
      />
      <Typography variant="h4" gutterBottom>
        Attempts / Logs {questionTitle && `for "${questionTitle}"`}
      </Typography>
      <NewButton onClick={() => handleOpen()} text="Add Log" />
      <QuestionHeader question={question} />
      <RecentAttemptsSummary logs={logs} />
      <LogList logs={logs} />

      {error && (
        <Typography color="error" sx={{ mb: 2 }}>
          {error}
        </Typography>
      )}

      <LogForm
        open={open}
        onClose={handleClose}
        onSave={handleSave}
        questionId={questionId}
        questionTitle={questionTitle}
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
