import React from 'react';
import PropTypes from 'prop-types';
import { Button } from '@mui/material';
import { ArrowBack } from '@mui/icons-material';

function BackButton({
  onClick,
  text = 'Back',
  sx = { mb: 2 },
  startIcon = <ArrowBack />,
  ...buttonProps
}) {
  return (
    <Button
      startIcon={startIcon}
      onClick={onClick}
      sx={sx}
      {...buttonProps}
    >
      {text}
    </Button>
  );
}

BackButton.propTypes = {
  onClick: PropTypes.func.isRequired,
  text: PropTypes.string,
  sx: PropTypes.object,
  startIcon: PropTypes.node,
};

export default BackButton;
