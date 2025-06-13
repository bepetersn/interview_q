import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
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
  Box,
  Chip,
} from '@mui/material';
import { Delete, Edit, Add } from '@mui/icons-material';
import api from '../api';

function QuestionLogList() {
  const { questionId } = useParams();
  const [logs, setLogs] = useState([]);
  const [questions, setQuestions] = useState([]);
  const [loading, setLoading] = useState(true);
  const [open, setOpen] = useState(false);
  const [editLog, setEditLog] = useState(null);
  const [form, setForm] = useState({
    question: questionId || '',
    date_attempted: '',
    time_spent_min: '',
    outcome: '',
    solution_approach: '',
    self_notes: '',
  });
  const [saving, setSaving] = useState(false);

  const fetchLogs = async () => {
    setLoading(true);
    try {
      const res = await api.get(`questions/${questionId}/logs/`);
      setLogs(res.data);
    } catch (e) {
      setLogs([]);
      console.error('Failed to fetch logs:', e);
    }
    setLoading(false);
  };

  const fetchQuestions = async () => {
    try {
      const res = await api.get('questions/');
      setQuestions(res.data);
    } catch (e) {
      setQuestions([]);
      console.error('Failed to fetch questions:', e);
    }
  };

  useEffect(() => {
    fetchLogs();
    fetchQuestions();
  }, [questionId]);

  const handleOpen = (log = null) => {
    setEditLog(log);
    setForm(log ? {
      ...log,
      question: log.question.id,
    } : {
      question: questionId || '', date_attempted: '', time_spent_min: '', outcome: '', solution_approach: '', self_notes: '',
    });
    setOpen(true);
  };

  const handleClose = () => {
    setOpen(false);
    setEditLog(null);
    setForm({ question: questionId || '', date_attempted: '', time_spent_min: '', outcome: '', solution_approach: '', self_notes: '' });
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setForm((f) => ({ ...f, [name]: value }));
  };

  const handleSave = async () => {
    setSaving(true);
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
      console.error('Failed to save log:', e);
    }
    setSaving(false);
  };

  const handleDelete = async (id) => {
    if (!window.confirm('Delete this log?')) return;
    await api.delete(`questions/${questionId}/logs/${id}/`);
    fetchLogs();
  };

  const question = questions.find(q => String(q.id) === String(questionId));

  return (
    <div>
      <Typography variant="h4" gutterBottom>Question Details</Typography>
      {question && (
        <Box mb={3} p={2} sx={{ background: '#f9f9f9', borderRadius: 2 }}>
          <Typography variant="h5" gutterBottom>{question.title}</Typography>
          <Typography variant="subtitle1" gutterBottom>Difficulty: {question.difficulty || 'N/A'}</Typography>
          {question.source && <Typography variant="body2" gutterBottom>Source: {question.source}</Typography>}
          {question.notes && <Typography variant="body1" gutterBottom>Notes: {question.notes}</Typography>}
          {question.tags && question.tags.length > 0 && (
            <Box mt={1}>
              <Typography variant="body2" component="span">Tags: </Typography>
              {question.tags.map((tag) => (
                <Chip key={tag.id || tag} label={tag.name || tag} size="small" sx={{ mr: 0.5 }} />
              ))}
            </Box>
          )}
        </Box>
      )}
      <Typography variant="h4" gutterBottom>Attempts / Logs</Typography>
      <Button variant="contained" startIcon={<Add />} onClick={() => handleOpen()} sx={{ mb: 2 }}>Add Log</Button>
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
                secondary={<>
                  <div>Date: {log.date_attempted}</div>
                  <div>Outcome: {log.outcome}</div>
                  <div>Time Spent: {log.time_spent_min} min</div>
                  <div>Approach: {log.solution_approach}</div>
                  <div>Notes: {log.self_notes}</div>
                </>}
              />
            </ListItem>
          ))}
        </List>
      )}
      <Dialog open={open} onClose={handleClose} maxWidth="sm" fullWidth>
        <DialogTitle>{editLog ? 'Edit Log' : 'Add Log'}</DialogTitle>
        <DialogContent>
          <FormControl fullWidth margin="dense">
            <InputLabel>Question</InputLabel>
            <Select name="question" value={form.question} label="Question" onChange={handleChange} disabled={!!questionId}>
              {questions.map((q) => (
                <MenuItem key={q.id} value={q.id}>{q.title}</MenuItem>
              ))}
            </Select>
          </FormControl>
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

export default QuestionLogList;
