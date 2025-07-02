import React, { useState } from 'react';
import PropTypes from 'prop-types';
import {
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
  MenuItem,
  Select,
  InputLabel,
  FormControl,
  Button,
  Typography,
} from '@mui/material';
import { getCurrentDateTimeLocalString } from '../../../utils';
import './LogForm.css';

function LogForm({
  open,
  onClose,
  onSave,
  questionId,
  questionTitle,
  error,
  saving
}) {
  const [form, setForm] = useState(() => {
    const currentDateTime = getCurrentDateTimeLocalString();

    return {
      question: questionId || '',
      date_attempted: currentDateTime,
      time_spent_min: '',
      outcome: '',
      solution_approach: '',
      self_notes: '',
    };
  });

  React.useEffect(() => {
    if (open) {
      const currentDateTime = getCurrentDateTimeLocalString();

      const newFormState = {
        question: questionId || '',
        date_attempted: currentDateTime,
        time_spent_min: '',
        outcome: '',
        solution_approach: '',
        self_notes: '',
      };
      setForm(newFormState);
    }
  }, [open, questionId]);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setForm((f) => ({ ...f, [name]: value }));
  };

  const handleSave = () => {
    onSave(form);
  };

  return (
    <Dialog open={open} onClose={onClose} maxWidth="sm" fullWidth>
      <DialogTitle>Add Log</DialogTitle>
      <DialogContent>
        {questionId ? (
          <Typography className="log-form-question-info">
            <b>Question:</b> {questionTitle}
          </Typography>
        ) : (
          <FormControl fullWidth margin="dense">
            <InputLabel>Question</InputLabel>
            <Select name="question" value={form.question} label="Question" onChange={handleChange}>
              {questionTitle && <MenuItem value={questionId}>{questionTitle}</MenuItem>}
            </Select>
          </FormControl>
        )}

        <TextField
          margin="dense"
          label="Date Attempted"
          name="date_attempted"
          type="datetime-local"
          value={form.date_attempted}
          onChange={handleChange}
          fullWidth
        />

        <TextField
          margin="dense"
          label="Time Spent (min)"
          name="time_spent_min"
          type="number"
          value={form.time_spent_min}
          onChange={handleChange}
          fullWidth
        />

        <FormControl fullWidth margin="dense">
          <InputLabel>Outcome</InputLabel>
          <Select
            name="outcome"
            value={form.outcome || ''}
            label="Outcome"
            onChange={handleChange}
          >
            <MenuItem value="">None</MenuItem>
            <MenuItem value="Solved">Solved</MenuItem>
            <MenuItem value="Partial">Partial</MenuItem>
            <MenuItem value="Failed">Failed</MenuItem>
          </Select>
        </FormControl>

        <TextField
          margin="dense"
          label="Solution Approach"
          name="solution_approach"
          value={form.solution_approach}
          onChange={handleChange}
          fullWidth
        />

        <TextField
          margin="dense"
          label="Notes"
          name="self_notes"
          value={form.self_notes}
          onChange={handleChange}
          fullWidth
          multiline
          rows={2}
        />

        {error && (
          <Typography color="error" className="log-form-error">
            {error}
          </Typography>
        )}
      </DialogContent>
      <DialogActions>
        <Button onClick={onClose}>Cancel</Button>
        <Button onClick={handleSave} disabled={saving}>
          {saving ? 'Saving...' : 'Save'}
        </Button>
      </DialogActions>
    </Dialog>
  );
}

LogForm.propTypes = {
  open: PropTypes.bool.isRequired,
  onClose: PropTypes.func.isRequired,
  onSave: PropTypes.func.isRequired,
  questionId: PropTypes.string,
  questionTitle: PropTypes.string,
  error: PropTypes.string,
  saving: PropTypes.bool,
};

export default LogForm;
