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
  FormControl
} from '@mui/material';
import { Add } from '@mui/icons-material';
import { useNavigate } from 'react-router-dom';
import api from '../api';
import TagList from './TagList.jsx';
import QuestionListItem from './QuestionListItem.jsx';

function QuestionList() {
  const [questions, setQuestions] = useState([]);
  const [tags, setTags] = useState([]);
  const [loading, setLoading] = useState(true);
  const [open, setOpen] = useState(false);
  const [editQuestion, setEditQuestion] = useState(null);
  const [form, setForm] = useState({
    title: '',
    source: '',
    notes: '',
    difficulty: '',
    topic_tags: [],
    is_active: true,
  });
  const [saving, setSaving] = useState(false);
  const [tagDialogOpen, setTagDialogOpen] = useState(false);
  const [error, setError] = useState("");
  const navigate = useNavigate();

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
    // Remove slug if present
    const { slug, ...rest } = question || {};
    setForm(question ? {
      ...rest,
      topic_tags: question.topic_tags ? question.topic_tags.map(t => t.id) : [],
    } : {
      title: '', source: '', notes: '', difficulty: '', topic_tags: [], is_active: true,
    });
    setOpen(true);
  };

  const handleClose = () => {
    setOpen(false);
    setEditQuestion(null);
    setForm({ title: '', source: '', notes: '', difficulty: '', topic_tags: [], is_active: true });
  };

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    setForm((f) => ({ ...f, [name]: type === 'checkbox' ? checked : value }));
  };

  const handleTagsChange = (e) => {
    setForm((f) => ({ ...f, topic_tags: e.target.value }));
  };

  const handleSave = async () => {
    setSaving(true);
    setError("");
    try {
      // Remove slug from payload if present
      const { slug, ...payload } = form;
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
            onViewLogs={(id) => navigate(`/logs/${id}`)}
          />
        ))}
      </List>
    );
  }

  return (
    <div>
      <Box display="flex" alignItems="center" justifyContent="space-between">
        <Typography variant="h4" gutterBottom>Questions</Typography>
        <Button variant="outlined" startIcon={<Add />} onClick={() => handleOpen()} sx={{ mb: 2 }}>Add Question</Button>
      </Box>
      <Button variant="text" onClick={() => setTagDialogOpen(true)} sx={{ mb: 2 }}>Manage Tags</Button>
      {error && (
        <Typography color="error" sx={{ mb: 2 }}>{error}</Typography>
      )}
      {renderQuestionsList()}
      {/* Question CRUD Dialog */}
      <Dialog open={open} onClose={handleClose} maxWidth="sm" fullWidth>
        <DialogTitle>{editQuestion ? 'Edit Question' : 'Add Question'}</DialogTitle>
        <DialogContent>
          <TextField margin="dense" label="Title" name="title" value={form.title} onChange={handleChange} fullWidth />
          <TextField margin="dense" label="Source" name="source" value={form.source} onChange={handleChange} fullWidth />
          <TextField margin="dense" label="Notes" name="notes" value={form.notes} onChange={handleChange} fullWidth multiline rows={2} />
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
              name="topic_tags"
              value={form.topic_tags}
              onChange={handleTagsChange}
              renderValue={(selected) => tags.filter(t => selected.includes(t.id)).map(t => t.name).join(', ')}
            >
              {tags.map((tag) => (
                <MenuItem key={tag.id} value={tag.id}>{tag.name}</MenuItem>
              ))}
            </Select>
          </FormControl>
          <FormControlLabel control={<Switch checked={form.is_active} name="is_active" onChange={handleChange} />} label="Active" />
        </DialogContent>
        <DialogActions>
          <Button onClick={handleClose}>Cancel</Button>
          <Button onClick={handleSave} disabled={saving || !form.title}>
            {saving ? 'Saving...' : 'Save'}
          </Button>
        </DialogActions>
      </Dialog>
      {/* Tag Management Dialog */}
      <Dialog open={tagDialogOpen} onClose={() => setTagDialogOpen(false)} maxWidth="sm" fullWidth>
        <DialogTitle>Manage Tags</DialogTitle>
        <DialogContent>
          <TagList embedded />
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setTagDialogOpen(false)}>Close</Button>
        </DialogActions>
      </Dialog>
    </div>
  );
}

export default QuestionList;
