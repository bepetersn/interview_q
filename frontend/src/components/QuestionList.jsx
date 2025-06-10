import React, { useEffect, useState } from 'react';
import { Typography, Button, List, ListItem, ListItemText, IconButton, Dialog, DialogTitle, DialogContent, DialogActions, TextField, Switch, FormControlLabel, CircularProgress, Chip, Box, MenuItem, Select, InputLabel, FormControl } from '@mui/material';
import { Delete, Edit, Add, ListAlt } from '@mui/icons-material';
import { useNavigate } from 'react-router-dom';
import api from '../api';
import TagList from './TagList.jsx';

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
  const navigate = useNavigate();

  const fetchQuestions = async () => {
    setLoading(true);
    try {
      const res = await api.get('questions/');
      setQuestions(res.data);
    } catch (e) {
      setQuestions([]);
    }
    setLoading(false);
  };

  const fetchTags = async () => {
    try {
      const res = await api.get('tags/');
      setTags(res.data);
    } catch (e) {
      setTags([]);
    }
  };

  useEffect(() => {
    fetchQuestions();
    fetchTags();
  }, []);

  const handleOpen = (question = null) => {
    setEditQuestion(question);
    setForm(question ? {
      ...question,
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
    try {
      const payload = { ...form };
      if (editQuestion) {
        await api.put(`questions/${editQuestion.id}/`, payload);
      } else {
        await api.post('questions/', payload);
      }
      fetchQuestions();
      handleClose();
    } catch (e) {}
    setSaving(false);
  };

  const handleDelete = async (id) => {
    if (!window.confirm('Delete this question?')) return;
    await api.delete(`questions/${id}/`);
    fetchQuestions();
  };

  return (
    <div>
      <Box display="flex" alignItems="center" justifyContent="space-between">
        <Typography variant="h4" gutterBottom>Questions</Typography>
        <Button variant="outlined" startIcon={<Add />} onClick={() => handleOpen()} sx={{ mb: 2 }}>Add Question</Button>
      </Box>
      <Button variant="text" onClick={() => setTagDialogOpen(true)} sx={{ mb: 2 }}>Manage Tags</Button>
      {loading ? <CircularProgress /> : (
        <List>
          {questions.map((q) => (
            <ListItem key={q.id} alignItems="flex-start" secondaryAction={
              <Box>
                <IconButton edge="end" onClick={() => handleOpen(q)}><Edit /></IconButton>
                <IconButton edge="end" onClick={() => handleDelete(q.id)}><Delete /></IconButton>
                <IconButton edge="end" onClick={() => navigate(`/logs/${q.id}`)} title="View Attempts"><ListAlt /></IconButton>
              </Box>
            }>
              <ListItemText
                primary={<Box>
                  <b>{q.title}</b> <Chip label={q.difficulty} size="small" sx={{ ml: 1 }} />
                </Box>}
                secondary={
                  <>
                    <span>{q.notes}</span><br/>
                    <span>
                      Tags:&nbsp;
                      {q.topic_tags && q.topic_tags.map(t => (
                        <Chip key={t.id} label={t.name} size="small" sx={{ mr: 0.5 }} component="span" />
                      ))}
                    </span><br/>
                    <span>Status: {q.is_active ? 'Active' : 'Inactive'}</span>
                  </>
                }
                slotProps={{ secondary: { component: 'div' } }}
              />
            </ListItem>
          ))}
        </List>
      )}
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
          <Button onClick={handleSave} disabled={saving}>{saving ? 'Saving...' : 'Save'}</Button>
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
