import { render, screen, waitFor } from '@testing-library/react';
import { MemoryRouter } from 'react-router-dom';
import QuestionList from '../QuestionList.jsx';
import api from '../../api';

jest.mock('../../api');

const mockQuestion = {
  id: 1,
  title: 'Sample Question',
  notes: 'Example',
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

  expect(api.get).toHaveBeenCalledWith('questions/');
  await waitFor(() => expect(api.get).toHaveBeenCalledWith('tags/'));
  expect(await screen.findByText('Sample Question')).toBeInTheDocument();
});
