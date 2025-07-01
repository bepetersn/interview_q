import React from 'react';
import { render, screen } from '@testing-library/react';
import { MemoryRouter } from 'react-router-dom';
import QuestionList from '../QuestionList.jsx';
import api from '../../api';

import { vi } from 'vitest';

vi.mock('../../api');

const mockQuestion = {
  id: 1,
  title: 'Sample Question',
  content: 'Example',
  difficulty: 'Easy',
  topic_tags: [],
  is_active: true,
};

const mockTag = { id: 1, name: 'Tag1' };

test('fetches and displays questions', async () => {
  api.get.mockResolvedValueOnce({ data: [mockQuestion] });
  api.get.mockResolvedValueOnce({ data: [mockTag] });

  render(
    <MemoryRouter>
      <QuestionList />
    </MemoryRouter>
  );

  expect(api.get).toHaveBeenNthCalledWith(1, 'questions/');
  expect(api.get).toHaveBeenNthCalledWith(2, 'tags/');
  expect(await screen.findByText('Sample Question')).toBeInTheDocument();
});
