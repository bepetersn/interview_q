import { render, screen } from '@testing-library/react';
import QuestionLogList from '../QuestionLogList.jsx';
import api from '../../api';

jest.mock('../../api');

jest.mock('react-router-dom', () => ({
  ...jest.requireActual('react-router-dom'),
  useParams: () => ({ questionId: '1' }),
}));

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

  expect(api.get).toHaveBeenNthCalledWith(1, 'questionlogs/', { params: { question: '1' } });
  expect(api.get).toHaveBeenNthCalledWith(2, 'questions/');
  expect(await screen.findByText('Question1')).toBeInTheDocument();
  expect(await screen.findByText('Outcome: Solved')).toBeInTheDocument();
});
