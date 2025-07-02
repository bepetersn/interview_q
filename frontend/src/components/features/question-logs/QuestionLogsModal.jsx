import React, { useState, useEffect } from 'react';
import { Modal, Box, IconButton, Paper } from '@mui/material';
import CloseIcon from '@mui/icons-material/Close';
import EditIcon from '@mui/icons-material/Edit';
import PropTypes from 'prop-types';
import QuestionLogList from './QuestionLogList.jsx';
import QuestionFormDialog from '../questions/QuestionFormDialog.jsx';
import { useQuestionForm } from '../../../hooks/useQuestionForm.js';
import api from '../../../api';
import './QuestionLogsModal.css';

function QuestionLogsModal({ open, onClose, question }) {
  const [localQuestion, setLocalQuestion] = useState(question);
  const [tags, setTags] = useState([]);
  const [error, setError] = useState('');

  const {
    open: editOpen,
    editQuestion,
    form,
    saving,
    setSaving,
    handleOpen,
    handleClose,
    handleFormChange,
    handleTagsChange
  } = useQuestionForm();

  useEffect(() => {
    setLocalQuestion(question);
  }, [question]);

  useEffect(() => {
    if (editOpen) {
      fetchTags();
    }
  }, [editOpen]);

  const fetchTags = async () => {
    try {
      const res = await api.get('tags/');
      setTags(res.data);
    } catch (e) {
      console.error('Error fetching tags:', e);
      setTags([]);
    }
  };

  const handleSave = async () => {
    if (!editQuestion) return;
    setSaving(true);
    setError('');

    try {
      const { slug, ...payload } = form;
      payload.tag_ids = (payload.tag_ids || []).filter(id => tags.some(t => t.id === id));
      await api.put(`questions/${editQuestion.id}/`, payload);
      setLocalQuestion({ ...localQuestion, ...payload });
      handleClose();
    } catch (e) {
      setError(e?.response?.data?.detail || e.message || 'Error saving question.');
    }

    setSaving(false);
  };

  return (
    <Modal open={open} onClose={onClose}>
      <Paper className="question-logs-modal-paper">
        {/* Header with close button */}
        <Box className="question-logs-modal-header">
          <IconButton onClick={() => handleOpen(localQuestion)} aria-label="edit">
            <EditIcon />
          </IconButton>
          <IconButton onClick={onClose} aria-label="close">
            <CloseIcon />
          </IconButton>
        </Box>

        {/* Scrollable content area */}
        <div className="question-logs-modal-content">
          {open && (
            <div className="question-logs-modal-inner">
              <QuestionLogList
                questionId={localQuestion?.id}
                embedded
                question={localQuestion}
                onClose={onClose}
              />
            </div>
          )}
        </div>

        <QuestionFormDialog
          open={editOpen}
          onClose={handleClose}
          editQuestion={editQuestion}
          form={form}
          onFormChange={handleFormChange}
          onTagsChange={handleTagsChange}
          onSave={handleSave}
          saving={saving}
          tags={tags}
        />

        {error && (
          <Box sx={{ p: 2 }}>
            <span style={{ color: 'red' }}>{error}</span>
          </Box>
        )}
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
