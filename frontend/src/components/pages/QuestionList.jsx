import React, { useState } from 'react';
import {
  QuestionListHeader,
  QuestionsDisplaySection,
  QuestionEditForm
} from '../features/questions/index.js';
import { TagManagementDialog } from '../features/tags/index.js';
import { QuestionLogsModal } from '../features/question-logs/index.js';
import { useQuestions } from '../../hooks/useQuestions.js';

// Helper to get initial form data for a new question
function getInitialFormData(sources) {
  return {
    title: "",
    source: sources[0],
    content: "",
    difficulty: "Easy",
    tag_ids: [],
    is_active: true,
  };
}

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

  const [tagDialogOpen, setTagDialogOpen] = useState(false);
  const [logsOpen, setLogsOpen] = useState(false);
  const [selectedQuestion, setSelectedQuestion] = useState(null);
  const [questionFormOpen, setQuestionFormOpen] = useState(false);
  const [formData, setFormData] = useState(getInitialFormData(sources));

  const handleDelete = async (id) => {
    setError("");
    const result = await deleteQuestion(id);

    if (!result.success && result.error) {
      setError(result.error);
    }
  };

  const handleViewLogs = (id) => {
    const question = questions.find(q => q.id === id);
    setSelectedQuestion(question);
    setLogsOpen(true);
  };

  const handleAddQuestion = () => {
    setQuestionFormOpen(true);
  };

  const handleFormChange = (field, value) => {
    setFormData((prevData) => ({
      ...prevData,
      [field]: value,
    }));
  };

  const handleTagsChange = (tags) => {
    setFormData((prevData) => ({
      ...prevData,
      tag_ids: tags,
    }));
  };

  const handleSave = async () => {
    try {
      const result = await saveQuestion(formData, false, null);
      if (result.success) {
        await fetchQuestions();
        setQuestionFormOpen(false);
      } else {
        console.error("Error saving question:", result.error);
      }
    } catch (error) {
      console.error("Unexpected error saving question:", error);
    }
  };

  return (
    <div>
      <QuestionListHeader
        onAddQuestion={handleAddQuestion}
        onManageTags={() => setTagDialogOpen(true)}
        error={error}
      />

      <QuestionsDisplaySection
        questions={questions}
        loading={loading}
        onDelete={handleDelete}
        onViewLogs={handleViewLogs}
      />

      {/* /////////////////
      // Dialogs
      ///////////////////// */}

      {/* for Tag Management */}
      <TagManagementDialog
        open={tagDialogOpen}
        onClose={() => setTagDialogOpen(false)}
        onTagsUpdated={fetchTags}
      />

      {/* for Question Logs */}
      <QuestionLogsModal
        isOpen={logsOpen}
        onClose={() => {
          setLogsOpen(false);
          setSelectedQuestion(null);
        }}
        question={selectedQuestion}
      />

      {/* for New Question */}
      <QuestionEditForm
        open={questionFormOpen}
        onClose={() => setQuestionFormOpen(false)}
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
