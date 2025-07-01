import React from 'react';
import PropTypes from 'prop-types';
import { Button } from '@mui/material';
import { Add } from '@mui/icons-material';

function NewButton({
  onClick,
  text = 'New',
  sx = { mb: 2 },
  startIcon = <Add />,
  variant = 'contained',
  ...buttonProps
}) {
  return (
    <Button
      variant={variant}
      startIcon={startIcon}
      onClick={onClick}
      sx={sx}
      {...buttonProps}
    >
      {text}
    </Button>
  );
}

NewButton.propTypes = {
  onClick: PropTypes.func.isRequired,
  text: PropTypes.string,
  sx: PropTypes.object,
  startIcon: PropTypes.node,
  variant: PropTypes.string,
};

export default NewButton;
