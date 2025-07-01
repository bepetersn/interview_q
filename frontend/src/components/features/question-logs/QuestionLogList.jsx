import React, { useEffect, useState } from 'react';
import PropTypes from 'prop-types';
import { useParams, useNavigate } from 'react-router-dom';
import {
  Typography,
  Button,
  List,
  ListItem,
  ListItemText,
  IconButton,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
  CircularProgress,
  MenuItem,
  Select,
  InputLabel,
  FormControl,
  Chip,
  Box,
} from '@mui/material';
import { Delete, Edit, Add, ArrowBack } from '@mui/icons-material';
import api from '../../../api';
import { getCurrentDateTimeLocalString } from '../../../utils';

function QuestionLogList({ questionId: propQuestionId, embedded = false, question: questionProp, onClose }) {
  const { questionId: paramQuestionId } = useParams();
  const questionId = propQuestionId || paramQuestionId;
  const navigate = useNavigate();
  const [logs, setLogs] = useState([]);
  const [question, setQuestion] = useState(questionProp || null);
  const [loading, setLoading] = useState(true);
  const [open, setOpen] = useState(false);
  const [editLog, setEditLog] = useState(null);
  const [form, setForm] = useState({
    question: questionId || '',
    date_attempted: getCurrentDateTimeLocalString(),
    time_spent_min: '',
    outcome: '',
    solution_approach: '',
    self_notes: '',
  });
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState('');

  const fetchLogs = async () => {
    setLoading(true);
    setError('');
    try {
      const res = await api.get(`questions/${questionId}/logs/`);
      setLogs(res.data);
    } catch (e) {
      setLogs([]);
      setError(e?.response?.data?.detail || e.message || 'Error fetching logs.');
    }
    setLoading(false);
  };

  const fetchQuestion = async () => {
    if (questionProp) return;
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
    fetchLogs();
    fetchQuestion();
  }, [questionId]);

  const handleOpen = (log = null) => {
    setEditLog(log);
    setForm(
      log
        ? {
            ...log,
            question: log.question.id,
          }
        : {
            question: questionId || '',
            date_attempted: getCurrentDateTimeLocalString(),
            time_spent_min: '',
            outcome: '',
            solution_approach: '',
            self_notes: '',
          },
    );
    setOpen(true);
  };

  const handleClose = () => {
    setOpen(false);
    setEditLog(null);
    setForm({
      question: questionId || '',
      date_attempted: getCurrentDateTimeLocalString(),
      time_spent_min: '',
      outcome: '',
      solution_approach: '',
      self_notes: '',
    });
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setForm((f) => ({ ...f, [name]: value }));
  };

  const handleSave = async () => {
    setSaving(true);
    setError('');
    try {
      const payload = { ...form };
      if (editLog) {
        await api.put(`questions/${questionId}/logs/${editLog.id}/`, payload);
      } else {
        await api.post(`questions/${questionId}/logs/`, payload);
      }
      fetchLogs();
      handleClose();
    } catch (e) {
      setError(e?.response?.data?.detail || e.message || 'Error saving log.');
      console.error('Error saving log:', e);
    }
    setSaving(false);
  };

  const handleDelete = async (id) => {
    if (!window.confirm('Delete this log?')) return;
    setError('');
    try {
      await api.delete(`questions/${questionId}/logs/${id}/`);
      fetchLogs();
    } catch (e) {
      setError(e?.response?.data?.detail || e.message || 'Error deleting log.');
    }
  };

  const questionTitle = question?.title;

  return (
    <div>
      <Button
        startIcon={<ArrowBack />}
        onClick={() => embedded ? onClose() : navigate('/')}
        sx={{ mb: 2 }}
      >
        {embedded ? 'Back' : 'Back to Questions'}
      </Button>
      <Typography variant="h4" gutterBottom>Attempts / Logs {questionTitle && `for "${questionTitle}"`}</Typography>
      <Button variant="contained" startIcon={<Add />} onClick={() => handleOpen()} sx={{ mb: 2 }}>Add Log</Button>
      {question && (
        <Box sx={{ textAlign: 'left', mb: 2 }}>
          <Typography variant="h6">{question.title}</Typography>
          {question.difficulty && <Chip label={question.difficulty} size="small" sx={{ ml: 1 }} />}
        </Box>
      )}
      {error && (
        <Typography color="error" sx={{ mb: 2 }}>{error}</Typography>
      )}
      {loading ? <CircularProgress /> : (
        <List>
          {logs.map((log) => (
            <ListItem key={log.id} alignItems="flex-start" secondaryAction={
              <>
                <IconButton edge="end" onClick={() => handleOpen(log)}><Edit /></IconButton>
                <IconButton edge="end" onClick={() => handleDelete(log.id)}><Delete /></IconButton>
              </>
            }>
              <ListItemText
                primary={<b>{log.question.title}</b>}
                secondary={
                  <>
                    <span style={{ display: 'block' }}>Date: {log.date_attempted}</span>
                    <span style={{ display: 'block' }}>Outcome: {log.outcome}</span>
                    <span style={{ display: 'block' }}>Time Spent: {log.time_spent_min} min</span>
                    <span style={{ display: 'block' }}>Approach: {log.solution_approach}</span>
                    <span style={{ display: 'block' }}>Notes: {log.self_notes}</span>
                  </>
                }
              />
            </ListItem>
          ))}
        </List>
      )}
      <Dialog open={open} onClose={handleClose} maxWidth="sm" fullWidth>
        <DialogTitle>{editLog ? 'Edit Log' : 'Add Log'}</DialogTitle>
        <DialogContent>
          {questionId ? (
            <Typography sx={{ mt: 1, mb: 1 }}><b>Question:</b> {questionTitle}</Typography>
          ) : (
            <FormControl fullWidth margin="dense">
              <InputLabel>Question</InputLabel>
              <Select name="question" value={form.question} label="Question" onChange={handleChange}>
                {question && <MenuItem value={question.id}>{question.title}</MenuItem>}
              </Select>
            </FormControl>
          )}
          <TextField margin="dense" label="Date Attempted" name="date_attempted" type="datetime-local" value={form.date_attempted} onChange={handleChange} fullWidth InputLabelProps={{ shrink: true }} />
          <TextField margin="dense" label="Time Spent (min)" name="time_spent_min" type="number" value={form.time_spent_min} onChange={handleChange} fullWidth />
          <FormControl fullWidth margin="dense">
            <InputLabel>Outcome</InputLabel>
            <Select name="outcome" value={form.outcome} label="Outcome" onChange={handleChange}>
              <MenuItem value="">None</MenuItem>
              <MenuItem value="Solved">Solved</MenuItem>
              <MenuItem value="Partial">Partial</MenuItem>
              <MenuItem value="Failed">Failed</MenuItem>
            </Select>
          </FormControl>
          <TextField margin="dense" label="Solution Approach" name="solution_approach" value={form.solution_approach} onChange={handleChange} fullWidth />
          <TextField margin="dense" label="Notes" name="self_notes" value={form.self_notes} onChange={handleChange} fullWidth multiline rows={2} />
        </DialogContent>
        <DialogActions>
          <Button onClick={handleClose}>Cancel</Button>
          <Button onClick={handleSave} disabled={saving}>{saving ? 'Saving...' : 'Save'}</Button>
        </DialogActions>
      </Dialog>
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
