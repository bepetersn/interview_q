import React from 'react';
import { render, screen } from '@testing-library/react';
import TagList from '../features/tags/TagList.jsx';
import api from '../../api';

import { vi } from 'vitest';

vi.mock('../../api');

test('fetches and displays tags', async () => {
  api.get.mockResolvedValueOnce({ data: [{ id: 1, name: 'Tag1', description: 'desc', is_active: true }] });

  render(<TagList />);

  expect(api.get).toHaveBeenCalledWith('tags/');
  expect(await screen.findByText('Tag1')).toBeInTheDocument();
});
