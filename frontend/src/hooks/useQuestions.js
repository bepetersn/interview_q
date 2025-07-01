import { useState, useEffect } from 'react';
import api from '../api';

export function useQuestions() {
  const [questions, setQuestions] = useState([]);
  const [tags, setTags] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const fetchQuestions = async () => {
    setLoading(true);
    try {
      const res = await api.get('questions/');
      setQuestions(res.data);
    } catch (e) {
      console.error("Error fetching questions:", e);
      setQuestions([]);
    }
    setLoading(false);
  };

  const fetchTags = async () => {
    try {
      const res = await api.get('tags/');
      setTags(res.data);
    } catch (e) {
      console.error("Error fetching tags:", e);
      setTags([]);
    }
  };

  const saveQuestion = async (questionData, isEdit, editQuestionId) => {
    try {
      const { slug, ...payload } = questionData;
      payload.tag_ids = (payload.tag_ids || []).filter(id => tags.some(t => t.id === id));

      if (!payload.title) {
        throw new Error('Title is required');
      }

      if (isEdit) {
        await api.put(`questions/${editQuestionId}/`, payload);
      } else {
        await api.post('questions/', payload);
      }

      await fetchQuestions();
      return { success: true };
    } catch (e) {
      const errorMessage = e?.response?.data?.detail || e.message || 'Error saving question.';
      return { success: false, error: errorMessage };
    }
  };

  const deleteQuestion = async (id) => {
    if (!window.confirm('Delete this question?')) return { success: false };

    try {
      await api.delete(`questions/${id}/`);
      await fetchQuestions();
      return { success: true };
    } catch (e) {
      const errorMessage = e?.response?.data?.detail || e.message || 'Error deleting question.';
      return { success: false, error: errorMessage };
    }
  };

  useEffect(() => {
    fetchQuestions();
    fetchTags();
  }, []);

  return {
    questions,
    tags,
    loading,
    error,
    setError,
    fetchQuestions,
    fetchTags,
    saveQuestion,
    deleteQuestion
  };
}
