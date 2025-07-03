import React, { useState, useCallback } from 'react';
import { Modal, Box, IconButton, Paper } from '@mui/material';
import CloseIcon from '@mui/icons-material/Close';
import EditIcon from '@mui/icons-material/Edit';
import PropTypes from 'prop-types';
import QuestionLogList from './QuestionLogList.jsx';
import QuestionEditForm from '../questions/QuestionEditForm.jsx';
import { useQuestionForm } from '../../../hooks/useQuestionForm.js';
import { useQuestions } from '../../../hooks/useQuestions.js';
import './QuestionLogsModal.css';

function QuestionLogsModal({ isOpen, onClose, question }) {
  // --- State ---
  const [error, setError] = useState('');

  // --- Hooks ---
  const {
    open: editOpen,
    questionBeingEdited,
    form,
    saving,
    setSaving,
    handleOpen,
    handleClose,
    handleFormChange,
  } = useQuestionForm();
  const { tags, putQuestion, sources } = useQuestions();

  // Helper to build payload
  function buildQuestionPayload(form, tags) {
    const { slug, ...payload } = form;
    payload.tag_ids = (payload.tag_ids || []).filter(id => tags.some(t => t.id === id));
    return payload;
  }

  const handleSave = useCallback(async () => {
    if (!questionBeingEdited) return;
    setSaving(true);
    setError('');
    try {
      const payload = buildQuestionPayload(form, tags);
      const result = await putQuestion(questionBeingEdited.id, payload);
      if (result.success) {
        handleClose();
      } else {
        setError(result.error);
      }
    } catch (e) {
      setError(e?.response?.data?.detail || e.message || 'Error saving question.');
    }
    setSaving(false);
  }, [questionBeingEdited, form, tags, setSaving, handleClose, putQuestion]);

  const handleTagsChange = (tagIds) => {
    handleFormChange('tag_ids', tagIds);
  };

  return (
    <Modal open={isOpen} onClose={onClose}>
      <Paper className="question-logs-modal-paper">

        {/* Header with close button */}
        <Box className="question-logs-modal-header">
          <IconButton onClick={() => handleOpen(question)} aria-label="edit">
            <EditIcon />
          </IconButton>
          <IconButton onClick={onClose} aria-label="close">
            <CloseIcon />
          </IconButton>
        </Box>

        {/* Scrollable content area */}
        <div className="question-logs-modal-content">
          <div className="question-logs-modal-inner">
            <QuestionLogList
              questionId={question?.id}
              question={question}
              onClose={onClose}
            />
          </div>
        </div>

        <QuestionEditForm
          open={editOpen}
          onClose={handleClose}
          questionBeingEdited={questionBeingEdited || {}}
          form={form || { title: '', source: '', content: '', difficulty: '', tag_ids: [], is_active: true }}
          onFormChange={handleFormChange}
          onSave={handleSave}
          saving={saving}
          tags={tags}
          sources={sources}
          onTagsChange={handleTagsChange}
        />
        {error && (
          <Box className="error-message-box">
            <span className="error-message">{error}</span>
          </Box>
        )}
      </Paper>
    </Modal>
  );
}

QuestionLogsModal.propTypes = {
  isOpen: PropTypes.bool.isRequired,
  onClose: PropTypes.func.isRequired,
  question: PropTypes.object,
};

export default QuestionLogsModal;
