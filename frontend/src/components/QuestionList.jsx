import React, { useEffect, useState } from 'react';
import {
  Typography,
  Button,
  List,
  CircularProgress,
  Box,
  MenuItem,
  Select,
  InputLabel,
  FormControl,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
  Checkbox,
  ListItemText
} from '@mui/material';
import { Add } from '@mui/icons-material';

import api from '../api';
import TagList from './TagList.jsx';
import QuestionListItem from './QuestionListItem.jsx';
import QuestionLogsDrawer from './QuestionLogsDrawer.jsx';

function QuestionList() {
  const [questions, setQuestions] = useState([]);
  const [tags, setTags] = useState([]);
  const [loading, setLoading] = useState(true);
  const [open, setOpen] = useState(false);
  const [editQuestion, setEditQuestion] = useState(null);
  const [form, setForm] = useState({
    title: '',
    source: '',
    content: '',
    difficulty: '',
    tag_ids: [],
    is_active: true,
  });
  const [saving, setSaving] = useState(false);
  const [tagDialogOpen, setTagDialogOpen] = useState(false);
  const [error, setError] = useState("");
  const [logsOpen, setLogsOpen] = useState(false);
  const [selectedQuestion, setSelectedQuestion] = useState(null);

  const emptyForm = {
    title: '',
    source: '',
    content: '',
    difficulty: '',
    tag_ids: [],
    is_active: true,
  };

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

  useEffect(() => {
    fetchQuestions();
    fetchTags();
  }, []);

  const handleOpen = (question = null) => {
    setEditQuestion(question);
    const { slug, ...rest } = question || {};
    setForm(question ? {
      ...rest,
      tag_ids: question.tags ? question.tags.map(t => t.id) : [],
    } : emptyForm);
    setOpen(true);
  };

  const handleClose = () => {
    setOpen(false);
    setEditQuestion(null);
    setForm(emptyForm);
  };

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    setForm((f) => ({ ...f, [name]: type === 'checkbox' ? checked : value }));
  };

  const handleTagsChange = (e) => {
    setForm((f) => ({ ...f, tag_ids: e.target.value }));
  };

  const handleSave = async () => {
    setSaving(true);
    setError("");
    try {
      const { slug, ...payload } = form;
      payload.tag_ids = (payload.tag_ids || []).filter(id => tags.some(t => t.id === id));
      if (!payload.title) throw new Error('Title is required');
      if (editQuestion) {
        await api.put(`questions/${editQuestion.id}/`, payload);
      } else {
        await api.post('questions/', payload);
      }
      fetchQuestions();
      handleClose();
    } catch (e) {
      setError(e?.response?.data?.detail || e.message || 'Error saving question.');
    }
    setSaving(false);
  };

  const handleDelete = async (id) => {
    if (!window.confirm('Delete this question?')) return;
    setError("");
    try {
      await api.delete(`questions/${id}/`);
      fetchQuestions();
    } catch (e) {
      setError(e?.response?.data?.detail || e.message || 'Error deleting question.');
    }
  };

  // Helper to render the questions list or empty/loading state
  function renderQuestionsList() {
    if (loading) {
      return <CircularProgress />;
    }
    if (questions.length === 0) {
      return (
        <Typography variant="body1" color="text.secondary" sx={{ mt: 2 }}>
          No questions found. Click "Add Question" to create your first one.
        </Typography>
      );
    }
    return (
      <List>
        {questions.map((q) => (
          <QuestionListItem
            key={q.id}
            question={q}
            onEdit={handleOpen}
            onDelete={handleDelete}
            onViewLogs={(id) => {
              const q = questions.find(qq => qq.id === id);
              setSelectedQuestion(q);
              setLogsOpen(true);
            }}
          />
        ))}
      </List>
    );
  }

  return (
    <div>
      <Box display="flex" flexDirection="column" alignItems="flex-start" mb={2}>
        <Typography variant="h4" gutterBottom sx={{ mb: 1, ml: 1 }}>Questions</Typography>
        <Button variant="outlined" startIcon={<Add />} onClick={() => handleOpen()} sx={{ mb: 1, ml: 1 }}>
          Add Question
        </Button>
      </Box>
      <Button variant="text" onClick={() => setTagDialogOpen(true)} sx={{ mb: 2, ml: 1 }}>Manage Tags</Button>
      {error && (
        <Typography color="error" sx={{ mb: 2, ml: 1 }}>{error}</Typography>
      )}
      <Box
        sx={{
          width: { xs: '100%', sm: '50vw' },
          maxWidth: { xs: '100%', sm: '50vw' },
          ml: 1,
          boxSizing: 'border-box',
        }}
      >
        {renderQuestionsList()}
      </Box>
      {/* Question CRUD Dialog */}
      <Dialog open={open} onClose={handleClose} maxWidth="sm" fullWidth>
        <DialogTitle>{editQuestion ? 'Edit Question' : 'Add Question'}</DialogTitle>
        <DialogContent>
          <TextField margin="dense" label="Title" name="title" value={form.title} onChange={handleChange} fullWidth />
          <TextField margin="dense" label="Source" name="source" value={form.source} onChange={handleChange} fullWidth />
          <TextField margin="dense" label="Content" name="content" value={form.content} onChange={handleChange} fullWidth multiline rows={2} />
          <FormControl fullWidth margin="dense">
            <InputLabel>Difficulty</InputLabel>
            <Select name="difficulty" value={form.difficulty} label="Difficulty" onChange={handleChange}>
              <MenuItem value="">None</MenuItem>
              <MenuItem value="Easy">Easy</MenuItem>
              <MenuItem value="Medium">Medium</MenuItem>
              <MenuItem value="Hard">Hard</MenuItem>
            </Select>
          </FormControl>
          <FormControl fullWidth margin="dense">
            <InputLabel>Tags</InputLabel>
            <Select
              multiple
              name="tag_ids"
              value={form.tag_ids}
              onChange={handleTagsChange}
              renderValue={(selected) => tags.filter(t => selected.includes(t.id)).map(t => t.name).join(', ')}
            >
              {tags.map((tag) => (
                <MenuItem key={tag.id} value={tag.id}>
                  <Checkbox checked={form.tag_ids.indexOf(tag.id) > -1} />
                  <ListItemText primary={tag.name} />
                </MenuItem>
              ))}
            </Select>
          </FormControl>
        </DialogContent>
        <DialogActions>
          <Button onClick={handleClose}>Cancel</Button>
          <Button onClick={handleSave} disabled={saving || !form.title}>
            {saving ? 'Saving...' : 'Save'}
          </Button>
        </DialogActions>
      </Dialog>
      {/* Tag Management Dialog */}
      <Dialog open={tagDialogOpen} onClose={() => {
  setTagDialogOpen(false);
  fetchTags(); // Re-fetch tags after closing tag management
}} maxWidth="sm" fullWidth>
        <DialogTitle>Manage Tags</DialogTitle>
        <DialogContent>
          <TagList embedded />
        </DialogContent>
        <DialogActions>
          <Button onClick={() => {
      setTagDialogOpen(false);
      fetchTags(); // Re-fetch tags after closing tag management
    }}>Close</Button>
        </DialogActions>
      </Dialog>
      <QuestionLogsDrawer
        open={logsOpen}
        onClose={() => { setLogsOpen(false); setSelectedQuestion(null); }}
        question={selectedQuestion}
      />
    </div>
  );
}

export default QuestionList;
