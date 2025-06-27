import React from 'react';
import { render, screen } from '@testing-library/react';
import QuestionLogList from '../QuestionLogList.jsx';
import api from '../../api';

import { vi } from 'vitest';

vi.mock('../../api');

vi.mock('react-router-dom', async () => {
  const actual = await vi.importActual('react-router-dom');
  return {
    ...actual,
    useParams: () => ({ questionId: '1' }),
  };
});

const mockLog = {
  id: 1,
  question: { id: 1, title: 'Question1' },
  date_attempted: '2024-01-01T00:00',
  time_spent_min: 30,
  outcome: 'Solved',
  solution_approach: '',
  self_notes: '',
};

test('fetches and displays question logs', async () => {
  api.get.mockResolvedValueOnce({ data: [mockLog] });
  api.get.mockResolvedValueOnce({ data: [{ id: 1, title: 'Question1' }] });

  render(<QuestionLogList />);

  expect(api.get).toHaveBeenNthCalledWith(1, 'questions/1/logs/');
  expect(api.get).toHaveBeenNthCalledWith(2, 'questions/');
  expect(await screen.findByText('Question1')).toBeInTheDocument();
  expect(await screen.findByText('Outcome: Solved')).toBeInTheDocument();
});

test('shows an error message when fetching logs fails', async () => {
  api.get.mockRejectedValueOnce(new Error('Network Error'));
  api.get.mockResolvedValueOnce({ data: [] });

  render(<QuestionLogList />);

  expect(api.get).toHaveBeenNthCalledWith(1, 'questions/1/logs/');
  expect(await screen.findByText('Network Error')).toBeInTheDocument();
});
