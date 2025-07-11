import React, { useEffect, useState } from 'react';
import type { Todo } from '../types/todo';
import TodoForm from './TodoForm';
import TodoItem from './TodoItem';
import * as api from '../services/api';

const TodoList: React.FC = () => {
  const [todos, setTodos] = useState<Todo[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  // Load all todos from backend
  const loadTodos = async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await api.fetchTodos();
      setTodos(data);
    } catch {
      setError('Failed to load todos');
    } finally {
      setLoading(false);
    }
  };

  // Load todos on mount
  useEffect(() => {
    loadTodos();
  }, []);

  // Handle new todo added from TodoForm
  // Receives the full Todo object returned from backend
  const handleAdd = (newTodo: Todo) => {
    setTodos((prev) => [newTodo, ...prev]);
  };

  // Toggle todo completed status
  const handleToggle = async (id: string) => {
    const todo = todos.find((t) => t.id === id);
    if (!todo) return;
    try {
      await api.toggleTodo(id);
      setTodos((prev) =>
        prev.map((t) =>
          t.id === id
            ? { ...t, status: t.status === 'completed' ? 'pending' : 'completed' }
            : t
        )
      );
    } catch {
      setError('Failed to update todo');
    }
  };

  // Delete todo
  const handleDelete = async (id: string) => {
    try {
      await api.deleteTodo(id);
      setTodos((prev) => prev.filter((t) => t.id !== id));
    } catch {
      setError('Failed to delete todo');
    }
  };

  if (loading) return <p>Loading...</p>;
  if (error) return <p style={{ color: 'red' }}>{error}</p>;

  return (
    <div className="max-w-md mx-auto p-4">
      <h2 className="text-2xl font-bold mb-4">Todo List 📝</h2>
      <TodoForm onTodoAdded={handleAdd} />
      <ul className="mt-4 space-y-2">
        {todos.map((todo) => (
          <TodoItem
            key={todo.id}
            todo={todo}
            toggleTodo={handleToggle}
            deleteTodo={handleDelete}
          />
        ))}
      </ul>
    </div>
  );
};

export default TodoList;
