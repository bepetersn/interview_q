import React, { act } from 'react';
import { render, screen, cleanup } from '@testing-library/react';
import QuestionLogList from '../features/question-logs/QuestionLogList.jsx';
import api from '../../api';

import { vi } from 'vitest';

// Clean up between tests
afterEach(() => {
  cleanup();
});

vi.mock('../../api');

vi.mock('react-router-dom', async () => {
  const actual = await vi.importActual('react-router-dom');
  return {
    ...actual,
    useParams: () => ({ questionId: '1' }),
    useNavigate: () => vi.fn(),
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
  api.get.mockResolvedValueOnce({ data: { id: 1, title: 'Question1' } });

  await act(async () => {
    render(<QuestionLogList />);
  });

  expect(api.get).toHaveBeenNthCalledWith(1, 'questions/1/logs/');
  expect(api.get).toHaveBeenNthCalledWith(2, 'questions/1/');

  // Look for the specific text that appears in the list item
  expect(await screen.findByText(/Attempts \/ Logs.*for "Question1"/)).toBeInTheDocument();
  expect(await screen.findByText('Solved')).toBeInTheDocument();
});


test('shows an error message when fetching logs fails', async () => {
  api.get.mockRejectedValueOnce(new Error('Network Error'));
  api.get.mockResolvedValueOnce({ data: { id: 1, title: 'Question1' } });

  await act(async () => {
    render(<QuestionLogList />);
  });

  expect(api.get).toHaveBeenNthCalledWith(1, 'questions/1/logs/');
  expect(await screen.findByText('Network Error')).toBeInTheDocument();
});

test('defaults date to today when opening add log dialog', async () => {
  api.get.mockResolvedValueOnce({ data: [] });
  api.get.mockResolvedValueOnce({ data: { id: 1, title: 'Question1' } });

  await act(async () => {
    render(<QuestionLogList />);
  });

  // Wait for the component to be fully loaded
  await screen.findByText('Add Log');

  // Open the add log dialog by clicking the button (not the dialog title)
  await act(async () => {
    screen.getByRole('button', { name: 'Add Log' }).click();
  });

  // Wait for the dialog to appear
  await screen.findByRole('dialog');

  // The dialog should be for adding a new log
  await screen.findByRole('dialog', { name: 'Add Log' });  // Dialog should have "Add Log" title

  // Wait for the form to initialize
  await new Promise(resolve => setTimeout(resolve, 200));

  const dateInput = screen.getByLabelText('Date Attempted');

  const today = new Date();
  const expectedDate = new Date(today.getTime() - today.getTimezoneOffset() * 60000)
    .toISOString()
    .slice(0, 10);

  // The date input should be populated with today's date
  expect(dateInput.value).toMatch(new RegExp(`^${expectedDate}T\\d{2}:\\d{2}$`));
});
