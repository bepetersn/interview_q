import React from 'react';
import PropTypes from 'prop-types';
import {
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Button
} from '@mui/material';
import TagList from './TagList.jsx';

function TagManagementDialog({ open, onClose, onTagsUpdated }) {
  const handleClose = () => {
    onClose();
    onTagsUpdated(); // Re-fetch tags after closing tag management
  };

  return (
    <Dialog open={open} onClose={handleClose} maxWidth="sm" fullWidth>
      <DialogTitle>Manage Tags</DialogTitle>
      <DialogContent>
        <TagList embedded />
      </DialogContent>
      <DialogActions>
        <Button onClick={handleClose}>Close</Button>
      </DialogActions>
    </Dialog>
  );
}

TagManagementDialog.propTypes = {
  open: PropTypes.bool.isRequired,
  onClose: PropTypes.func.isRequired,
  onTagsUpdated: PropTypes.func.isRequired,
};

export default TagManagementDialog;
