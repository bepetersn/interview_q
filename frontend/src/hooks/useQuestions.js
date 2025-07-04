import { useState, useEffect } from 'react';
import api from '../api';
import { QUESTION_SOURCES } from '../constants.js';

/**
 * Custom hook for managing questions, tags, and related operations
 * @returns {Object} Hook state and methods
 */
export function useQuestions() {
  const [questions, setQuestions] = useState([]);
  const [tags, setTags] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  /**
   * Extract error message from API response
   * @param {Error} error - API error object
   * @returns {string} User-friendly error message
   */
  const getErrorMessage = (error) => {
    return error?.response?.data?.detail || error.message || 'An unexpected error occurred';
  };

  /**
   * Fetch questions from API
   * @returns {Promise<void>}
   */
  const fetchQuestions = async () => {
    setLoading(true);
    setError("");
    try {
      const res = await api.get('questions/');
      setQuestions(res.data);
    } catch (error) {
      console.error("Error fetching questions:", error);
      setError(getErrorMessage(error));
      setQuestions([]);
    } finally {
      setLoading(false);
    }
  };

  /**
   * Fetch tags from API
   * @returns {Promise<void>}
   */
  const fetchTags = async () => {
    setError("");
    try {
      const res = await api.get('tags/');
      setTags(res.data);
    } catch (error) {
      console.error("Error fetching tags:", error);
      setError(getErrorMessage(error));
      setTags([]);
    }
  };

  /**
   * Save or update a question
   * @param {Object} questionData - Question data to save
   * @param {boolean} isEdit - Whether this is an edit operation
   * @param {number|null} questionBeingEditedId - ID of question being edited
   * @returns {Promise<{success: boolean, error?: string}>}
   */
  const saveQuestion = async (questionData, isEdit, questionBeingEditedId) => {
    try {
      const { slug, ...payload } = questionData;
      payload.tag_ids = (payload.tag_ids || []).filter(id => tags.some(t => t.id === id));

      if (!payload.title?.trim()) {
        throw new Error('Title is required');
      }

      if (isEdit && !questionBeingEditedId) {
        throw new Error('Question ID is required for edit operations');
      }

      const endpoint = isEdit ? `questions/${questionBeingEditedId}/` : 'questions/';
      const method = isEdit ? 'put' : 'post';

      await api[method](endpoint, payload);
      await fetchQuestions();
      return { success: true };
    } catch (error) {
      const errorMessage = getErrorMessage(error);
      console.error("Error saving question:", error);
      return { success: false, error: errorMessage };
    }
  };

  /**
   * Update a question and return the updated question object
   * @param {number} id - Question ID
   * @param {Object} payload - Data to update
   * @returns {Promise<{success: boolean, data?: Object, error?: string}>}
   */
  const putQuestion = async (id, payload) => {
    try {
      const response = await api.put(`questions/${id}/`, payload);
      await fetchQuestions();
      return { success: true, data: response.data };
    } catch (error) {
      const errorMessage = getErrorMessage(error);
      console.error("Error updating question:", error);
      return { success: false, error: errorMessage };
    }
  };

  /**
   * Delete a question with confirmation
   * @param {number} id - Question ID to delete
   * @returns {Promise<{success: boolean, error?: string}>}
   */
  const deleteQuestion = async (id) => {
    if (!window.confirm('Delete this question?')) {
      return { success: false };
    }

    try {
      await api.delete(`questions/${id}/`);
      await fetchQuestions();
      return { success: true };
    } catch (error) {
      const errorMessage = getErrorMessage(error);
      console.error("Error deleting question:", error);
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
    deleteQuestion,
    putQuestion,
    sources: QUESTION_SOURCES
  };
}
