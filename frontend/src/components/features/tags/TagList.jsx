import React, { useEffect, useState } from 'react';
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
  Switch,
  FormControlLabel,
  CircularProgress,
} from '@mui/material';
import { Delete, Edit, Add } from '@mui/icons-material';
import api from '../../../api';

function TagList() {
  const [tags, setTags] = useState([]);
  const [loading, setLoading] = useState(true);
  const [open, setOpen] = useState(false);
  const [editTag, setEditTag] = useState(null);
  const [form, setForm] = useState({ name: '', description: '', is_active: true });
  const [saving, setSaving] = useState(false);

  const fetchTags = async () => {
    setLoading(true);
    try {
      const res = await api.get('tags/');
      setTags(res.data);
    } catch (e) {
      setTags([]);
      console.error('Failed to fetch tags: ', e);
    }
    setLoading(false);
  };

  useEffect(() => {
    fetchTags();
  }, []);

  const handleOpen = (tag = null) => {
    setEditTag(tag);
    setForm(tag ? { ...tag } : { name: '', description: '', is_active: true });
    setOpen(true);
  };

  const handleClose = () => {
    setOpen(false);
    setEditTag(null);
    setForm({ name: '', description: '', is_active: true });
  };

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    setForm((f) => ({ ...f, [name]: type === 'checkbox' ? checked : value }));
  };

  const handleSave = async () => {
    setSaving(true);
    try {
      if (editTag) {
        await api.put(`tags/${editTag.id}/`, form);
      } else {
        await api.post('tags/', form);
      }
      fetchTags();
      handleClose();
    } catch (e) {
      console.error('Failed to save tag: ', e);
    }
    setSaving(false);
  };

  const handleDelete = async (id) => {
    if (!window.confirm('Delete this tag?')) return;
    await api.delete(`tags/${id}/`);
    fetchTags();
  };

  return (
    <div>
      <Typography variant="h4" gutterBottom>Tags</Typography>
      <Button variant="contained" startIcon={<Add />} onClick={() => handleOpen()} sx={{ mb: 2 }}>Add Tag</Button>
      {loading ? <CircularProgress /> : (
        <List>
          {tags.map((tag) => (
            <ListItem key={tag.id} secondaryAction={
              <>
                <IconButton edge="end" onClick={() => handleOpen(tag)}><Edit /></IconButton>
                <IconButton edge="end" onClick={() => handleDelete(tag.id)}><Delete /></IconButton>
              </>
            }>
              <ListItemText primary={tag.name} secondary={tag.description} />
            </ListItem>
          ))}
        </List>
      )}
      <Dialog open={open} onClose={handleClose}>
        <DialogTitle>{editTag ? 'Edit Tag' : 'Add Tag'}</DialogTitle>
        <DialogContent>
          <TextField margin="dense" label="Name" name="name" value={form.name} onChange={handleChange} fullWidth />
          <TextField margin="dense" label="Description" name="description" value={form.description} onChange={handleChange} fullWidth />
          <FormControlLabel control={<Switch checked={form.is_active} name="is_active" onChange={handleChange} />} label="Active" />
        </DialogContent>
        <DialogActions>
          <Button onClick={handleClose}>Cancel</Button>
          <Button onClick={handleSave} disabled={saving}>{saving ? 'Saving...' : 'Save'}</Button>
        </DialogActions>
      </Dialog>
    </div>
  );
}

export default TagList;
