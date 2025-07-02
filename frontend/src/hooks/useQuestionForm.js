import { useState } from 'react';

const initialFormState = {
  title: '',
  source: '',
  content: '',
  difficulty: '',
  tag_ids: [],
  is_active: true,
};

export function useQuestionForm() {
  const [open, setOpen] = useState(false);
  const [questionBeingEdited, setQuestionBeingEdited] = useState(null);
  const [form, setForm] = useState(initialFormState);
  const [saving, setSaving] = useState(false);

  const handleOpen = (question = null) => {
    setQuestionBeingEdited(question);
    const { slug, ...rest } = question || {};
    setForm(question ? {
      ...rest,
      tag_ids: question.tags ? question.tags.map(t => t.id) : [],
    } : initialFormState);
    setOpen(true);
  };

  const handleClose = () => {
    setOpen(false);
    setQuestionBeingEdited(null);
    setForm(initialFormState);
  };

  const handleFormChange = (name, value) => {
    setForm((f) => ({ ...f, [name]: value }));
  };

  const handleTagsChange = (tagIds) => {
    setForm((f) => ({ ...f, tag_ids: tagIds }));
  };

  return {
    open,
    questionBeingEdited,
    form,
    saving,
    setSaving,
    handleOpen,
    handleClose,
    handleFormChange,
    handleTagsChange
  };
}
