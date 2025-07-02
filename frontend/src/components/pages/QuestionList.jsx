import React, { useState } from 'react';

import {
  QuestionFormDialog,
  QuestionListHeader,
  QuestionsDisplaySection
} from '../features/questions/index.js';
import { TagManagementDialog } from '../features/tags/index.js';
import { QuestionLogsModal } from '../features/question-logs/index.js';
import { useQuestions } from '../../hooks/useQuestions.js';
import { useQuestionForm } from '../../hooks/useQuestionForm.js';

function QuestionList() {
  // Use custom hooks
  const {
    questions,
    tags,
    loading,
    error,
    setError,
    fetchTags,
    saveQuestion,
    deleteQuestion
  } = useQuestions();

  const {
    open,
    editQuestion,
    form,
    saving,
    setSaving,
    handleOpen,
    handleClose,
    handleFormChange,
    handleTagsChange
  } = useQuestionForm();

  // Local state for dialogs and logs
  const [tagDialogOpen, setTagDialogOpen] = useState(false);
  const [logsOpen, setLogsOpen] = useState(false);
  const [selectedQuestion, setSelectedQuestion] = useState(null);

  // Handle save operation
  const handleSave = async () => {
    setSaving(true);
    setError("");

    const result = await saveQuestion(form, !!editQuestion, editQuestion?.id);

    if (result.success) {
      handleClose();
    } else {
      setError(result.error);
    }

    setSaving(false);
  };

  // Handle delete operation
  const handleDelete = async (id) => {
    setError("");
    const result = await deleteQuestion(id);

    if (!result.success && result.error) {
      setError(result.error);
    }
  };

  // Handle viewing logs
  const handleViewLogs = (id) => {
    const question = questions.find(q => q.id === id);
    setSelectedQuestion(question);
    setLogsOpen(true);
  };

  return (
    <div>
      <QuestionListHeader
        onAddQuestion={() => handleOpen()}
        onManageTags={() => setTagDialogOpen(true)}
        error={error}
      />

      <QuestionsDisplaySection
        questions={questions}
        loading={loading}
        onEdit={handleOpen}
        onDelete={handleDelete}
        onViewLogs={handleViewLogs}
      />

      <QuestionFormDialog
        open={open}
        onClose={handleClose}
        editQuestion={editQuestion}
        form={form}
        onFormChange={handleFormChange}
        onTagsChange={handleTagsChange}
        onSave={handleSave}
        saving={saving}
        tags={tags}
      />

      <TagManagementDialog
        open={tagDialogOpen}
        onClose={() => setTagDialogOpen(false)}
        onTagsUpdated={fetchTags}
      />

      <QuestionLogsModal
        open={logsOpen}
        onClose={() => { setLogsOpen(false); setSelectedQuestion(null); }}
        question={selectedQuestion}
      />
    </div>
  );
}

export default QuestionList;
