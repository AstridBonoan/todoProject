// src/components/TodoForm.tsx

import React, { useState } from "react";
import Input from "./Input";
import Button from "./Button";
import type { Todo } from "../types/todo";

interface TodoFormProps {
  /** Called after successful POST, receives the new todo object */
  onTodoAdded?: (newTodo: Todo) => void;
}

const TodoForm: React.FC<TodoFormProps> = ({ onTodoAdded }) => {
  const [inputValue, setInputValue] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  const handleAdd = async () => {
    if (!inputValue.trim()) {
      setError("Task cannot be empty");
      return;
    }

    setLoading(true);
    setError(null);

    try {
      const res = await fetch("http://127.0.0.1:5000/api/todos/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          task: inputValue,
          user_id: 1,
        }),
      });

      if (!res.ok) {
        const textResponse = await res.text();
        setError(`Failed to add todo: ${textResponse || res.statusText}`);
        return;
      }

      const newTodo: Todo = await res.json();
      console.log("New todo created:", newTodo);

      setInputValue("");
      setError(null);

      onTodoAdded?.(newTodo); // notify parent with the returned todo
    } catch (err) {
      console.error("Add todo error:", err);
      setError("Failed to add todo (network or CORS error)");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex items-center space-x-2">
      <Input
        value={inputValue}
        onChange={(e) => setInputValue(e.target.value)}
        placeholder="Add a new task"
        disabled={loading}
      />
      <Button onClick={handleAdd} disabled={loading}>
        {loading ? "Adding..." : "Add"}
      </Button>
      {error && <div className="text-red-500 text-sm mt-1">{error}</div>}
    </div>
  );
};

export default TodoForm;
