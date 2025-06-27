import React from 'react';
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import QuestionListItem from '../QuestionListItem.jsx';
import { vi } from 'vitest';

const question = {
  id: 1,
  title: 'Sample Question',
  notes: '',
  difficulty: 'Easy',
  tags: [],
};

test('title span acts as link to view logs', async () => {
  const onViewLogs = vi.fn();
  render(
    <QuestionListItem
      question={question}
      onEdit={vi.fn()}
      onDelete={vi.fn()}
      onViewLogs={onViewLogs}
    />
  );

  const link = screen.getByRole('link', {
    name: `View logs for ${question.title}`,
  });
  expect(link).toBeInTheDocument();

  link.focus();
  await userEvent.keyboard('{Enter}');
  expect(onViewLogs).toHaveBeenCalledWith(question.id);
});
