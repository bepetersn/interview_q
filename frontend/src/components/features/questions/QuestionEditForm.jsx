import React from 'react';
import PropTypes from 'prop-types';
import {
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
  Button,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Checkbox,
  ListItemText
} from '@mui/material';


const getContentPlaceholder = (form) => {
  if (form.source === "CodeWars" || !form.source) {
    return "<p>Example content</p><ul><li>Point 1</li><li>Point 2</li></ul>";
  }
  return `Example for ${form.source}`;
};


function QuestionEditForm({
  open,
  onClose,
  questionBeingEdited,
  form,
  onFormChange,
  onSave,
  saving,
  tags = [],
  sources = [],
  onTagsChange,
}) {
  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    onFormChange(name, type === 'checkbox' ? checked : value);
  };

  const handleTagsChangeLocal = (e) => {
    if (onTagsChange) {
      onTagsChange(e.target.value);
    }
  };

  return (
    <Dialog open={open} onClose={onClose} maxWidth="sm" fullWidth>
      <DialogTitle>{questionBeingEdited ? 'Edit Question' : 'Add Question'}</DialogTitle>
      <DialogContent>
        <TextField
          margin="dense"
          label="Title"
          name="title"
          value={form.title || ''}
          onChange={handleChange}
          fullWidth
        />
        <FormControl fullWidth margin="dense">
          <InputLabel shrink>Source</InputLabel> {/* Ensures the label doesn't overlap the placeholder */}
          <Select
            name="source"
            value={form.source || (sources[0] || '')}
            label="Source"
            onChange={handleChange}
            displayEmpty
          >
            {(Array.isArray(sources) ? sources : []).map((source) => (
              <MenuItem key={source} value={source}>{source}</MenuItem>
            ))}
          </Select>
        </FormControl>
        {form.source === "Other" && (
          <TextField
            margin="dense"
            label="Custom Source"
            name="customSource"
            value={form.customSource || ""}
            onChange={handleChange}
            fullWidth
          />
        )}
        <TextField
          margin="dense"
          label="Content"
          name="content"
          placeholder={getContentPlaceholder(form)}
          value={form.content || ''}
          onChange={handleChange}
          fullWidth
          multiline
          rows={2}
          slotProps={{
            inputLabel: { shrink: true },
          }}
        />
        <FormControl fullWidth margin="dense">
          <InputLabel>Difficulty</InputLabel>
          <Select
            name="difficulty"
            value={form.difficulty}
            label="Difficulty"
            onChange={handleChange}
          >
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
            value={form.tag_ids || []}
            onChange={handleTagsChangeLocal}
            renderValue={(selected) =>
              tags.filter(t => selected.includes(t.id)).map(t => t.name).join(', ')
            }
          >
            {tags.map((tag) => (
              <MenuItem key={tag.id} value={tag.id}>
                <Checkbox checked={(form.tag_ids || []).indexOf(tag.id) > -1} />
                <ListItemText primary={tag.name} />
              </MenuItem>
            ))}
          </Select>
        </FormControl>
      </DialogContent>
      <DialogActions>
        <Button onClick={onClose}>Cancel</Button>
        <Button onClick={onSave} disabled={saving || !form.title}>
          {saving ? 'Saving...' : 'Save'}
        </Button>
      </DialogActions>
    </Dialog>
  );
}

QuestionEditForm.propTypes = {
  open: PropTypes.bool.isRequired,
  onClose: PropTypes.func.isRequired,
  questionBeingEdited: PropTypes.object,
  form: PropTypes.shape({
    title: PropTypes.string.isRequired,
    source: PropTypes.string.isRequired,
    content: PropTypes.string.isRequired,
    difficulty: PropTypes.string.isRequired,
    tag_ids: PropTypes.array.isRequired,
    is_active: PropTypes.bool.isRequired,
    customSource: PropTypes.string,
  }).isRequired,
  onFormChange: PropTypes.func.isRequired,
  onSave: PropTypes.func.isRequired,
  saving: PropTypes.bool.isRequired,
  tags: PropTypes.array,
  sources: PropTypes.array,
  onTagsChange: PropTypes.func,
};

export default QuestionEditForm;
