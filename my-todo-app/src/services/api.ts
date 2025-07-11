import type { Todo } from '../types/todo';

const API_URL = 'http://localhost:5000/api';

export const fetchTodos = async (): Promise<Todo[]> => {
  const res = await fetch(`${API_URL}/todos/`);
  if (!res.ok) throw new Error('Failed to fetch todos');
  return res.json();
};

export const addTodo = async (text: string): Promise<Todo> => {
  const res = await fetch(`${API_URL}/todos/`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ task: text, user_id: 1 }),
  });
  if (!res.ok) throw new Error('Failed to add todo');
  return res.json();
};

export const toggleTodo = async (id: string): Promise<Todo> => {
  const res = await fetch(`${API_URL}/todos/${id}/toggle`, {
    method: 'PATCH',
  });
  if (!res.ok) throw new Error('Failed to update todo');
  return res.json();
};

export const deleteTodo = async (id: string): Promise<void> => {
  const res = await fetch(`${API_URL}/todos/${id}`, { method: 'DELETE' });
  if (!res.ok) throw new Error('Failed to delete todo');
};
