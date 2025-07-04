import React, { useState, useCallback } from 'react';
import {
  QuestionListHeader,
  QuestionsDisplaySection,
  QuestionEditForm
} from '../features/questions/index.js';
import { TagManagementDialog } from '../features/tags/index.js';
import { QuestionLogsModal } from '../features/question-logs/index.js';
import { useQuestions } from '../../hooks/useQuestions.js';

/**
 * Helper to get initial form data for a new question
 * @param {string[]} sources - Available question sources
 * @returns {Object} Initial form data
 */
const getInitialFormData = (sources) => ({
  title: "",
  source: sources[0] || "",
  content: "",
  difficulty: "Easy",
  tag_ids: [],
  is_active: true,
});

/**
 * Custom hook for managing dialog states
 * @returns {Object} Dialog state and handlers
 */
const useDialogStates = () => {
  const [tagDialogOpen, setTagDialogOpen] = useState(false);
  const [logsOpen, setLogsOpen] = useState(false);
  const [questionFormOpen, setQuestionFormOpen] = useState(false);
  const [selectedQuestion, setSelectedQuestion] = useState(null);

  const openTagDialog = useCallback(() => setTagDialogOpen(true), []);
  const closeTagDialog = useCallback(() => setTagDialogOpen(false), []);

  const openLogsDialog = useCallback((question) => {
    setSelectedQuestion(question);
    setLogsOpen(true);
  }, []);

  const closeLogsDialog = useCallback(() => {
    setLogsOpen(false);
    setSelectedQuestion(null);
  }, []);

  const openQuestionForm = useCallback(() => setQuestionFormOpen(true), []);
  const closeQuestionForm = useCallback(() => setQuestionFormOpen(false), []);

  return {
    tagDialogOpen,
    logsOpen,
    questionFormOpen,
    selectedQuestion,
    openTagDialog,
    closeTagDialog,
    openLogsDialog,
    closeLogsDialog,
    openQuestionForm,
    closeQuestionForm,
  };
};

/**
 * Main component for displaying and managing questions
 * @returns {JSX.Element} Question list page
 */
function QuestionList() {
  const {
    questions,
    tags,
    loading,
    error,
    setError,
    fetchTags,
    deleteQuestion,
    fetchQuestions,
    saveQuestion,
    sources,
  } = useQuestions();

  const {
    tagDialogOpen,
    logsOpen,
    questionFormOpen,
    selectedQuestion,
    openTagDialog,
    closeTagDialog,
    openLogsDialog,
    closeLogsDialog,
    openQuestionForm,
    closeQuestionForm,
  } = useDialogStates();

  const [formData, setFormData] = useState(() => getInitialFormData(sources));

  /**
   * Handle question deletion with error handling
   * @param {number} id - Question ID to delete
   */
  const handleDelete = useCallback(async (id) => {
    setError("");
    const result = await deleteQuestion(id);

    if (!result.success && result.error) {
      setError(result.error);
    }
  }, [deleteQuestion, setError]);

  /**
   * Handle viewing question logs
   * @param {number} id - Question ID
   */
  const handleViewLogs = useCallback((id) => {
    const question = questions.find(q => q.id === id);
    if (question) {
      openLogsDialog(question);
    }
  }, [questions, openLogsDialog]);

  /**
   * Handle form field changes
   * @param {string} field - Field name
   * @param {any} value - New value
   */
  const handleFormChange = useCallback((field, value) => {
    setFormData((prevData) => ({
      ...prevData,
      [field]: value,
    }));
  }, []);

  /**
   * Handle tags change specifically
   * @param {number[]} tags - Array of tag IDs
   */
  const handleTagsChange = useCallback((tags) => {
    setFormData((prevData) => ({
      ...prevData,
      tag_ids: tags,
    }));
  }, []);

  /**
   * Handle saving a new question
   */
  const handleSave = useCallback(async () => {
    try {
      const result = await saveQuestion(formData, false, null);
      if (result.success) {
        await fetchQuestions();
        closeQuestionForm();
        setFormData(getInitialFormData(sources)); // Reset form
      } else {
        console.error("Error saving question:", result.error);
        setError(result.error);
      }
    } catch (error) {
      console.error("Unexpected error saving question:", error);
      setError("An unexpected error occurred while saving the question");
    }
  }, [formData, saveQuestion, fetchQuestions, closeQuestionForm, sources, setError]);

  /**
   * Handle opening the add question form
   */
  const handleAddQuestion = useCallback(() => {
    setFormData(getInitialFormData(sources));
    openQuestionForm();
  }, [sources, openQuestionForm]);

  return (
    <div>
      <QuestionListHeader
        onAddQuestion={handleAddQuestion}
        onManageTags={openTagDialog}
        error={error}
      />

      <QuestionsDisplaySection
        questions={questions}
        loading={loading}
        onDelete={handleDelete}
        onViewLogs={handleViewLogs}
      />

      {/* Dialog Components */}
      <TagManagementDialog
        open={tagDialogOpen}
        onClose={closeTagDialog}
        onTagsUpdated={fetchTags}
      />

      <QuestionLogsModal
        isOpen={logsOpen}
        onClose={closeLogsDialog}
        question={selectedQuestion}
      />

      <QuestionEditForm
        open={questionFormOpen}
        onClose={closeQuestionForm}
        questionBeingEdited={null}
        form={formData}
        onFormChange={handleFormChange}
        onSave={handleSave}
        saving={false}
        tags={tags}
        sources={sources}
        onTagsChange={handleTagsChange}
      />
    </div>
  );
}

export default QuestionList;
