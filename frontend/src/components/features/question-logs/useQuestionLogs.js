import { useState, useEffect } from 'react';
import api from '../../../api';

export function useQuestionLogs(questionId, questionProp) {
  const [logs, setLogs] = useState([]);
  const [question, setQuestion] = useState(questionProp || null);
  const [error, setError] = useState('');

  const fetchLogs = async () => {
    setError('');
    try {
      const res = await api.get(`questions/${questionId}/logs/`);
      setLogs(res.data);
    } catch (e) {
      setLogs([]);
      setError(e?.response?.data?.detail || e.message || 'Error fetching logs.');
    }
  };

  const fetchQuestion = async () => {
    // If we have questionProp (from the drawer), use it - it already has all the data we need
    if (questionProp) {
      setQuestion(questionProp);
      return;
    }

    // Only fetch if we don't have questionProp (standalone usage)
    setError('');
    try {
      const res = await api.get(`questions/${questionId}/`);
      setQuestion(res.data);
    } catch (e) {
      setQuestion(null);
      setError(e?.response?.data?.detail || e.message || 'Error fetching question.');
    }
  };

  useEffect(() => {
    if (questionId) {
      fetchLogs();
      fetchQuestion();
    }
  }, [questionId]);

  const saveLog = async (formData, editLog) => {
    setError('');
    try {
      const payload = { ...formData };
      if (editLog) {
        await api.put(`questions/${questionId}/logs/${editLog.id}/`, payload);
      } else {
        await api.post(`questions/${questionId}/logs/`, payload);
      }
      await fetchLogs();
      return true;
    } catch (e) {
      setError(e?.response?.data?.detail || e.message || 'Error saving log.');
      console.error('Error saving log:', e);
      return false;
    }
  };

  return {
    logs,
    question,
    error,
    setError,
    saveLog,
    fetchLogs,
  };
}
