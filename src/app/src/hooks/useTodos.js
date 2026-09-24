import { useCallback, useEffect, useState } from 'react';

import { createTodo, deleteAllTodos, fetchTodos } from '../api/todos';

export function useTodos() {
  const [todos, setTodos] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);

  const loadTodos = useCallback(async (signal) => {
    setIsLoading(true);
    try {
      setTodos(await fetchTodos({ signal }));
      setError(null);
    } catch (err) {
      if (err.name === 'AbortError') return;
      setError(err.message);
    } finally {
      if (!signal?.aborted) setIsLoading(false);
    }
  }, []);

  useEffect(() => {
    const controller = new AbortController();
    loadTodos(controller.signal);
    return () => controller.abort();
  }, [loadTodos]);

  const addTodo = useCallback(
    async (description) => {
      await createTodo(description);
      await loadTodos();
    },
    [loadTodos],
  );

  const clearTodos = useCallback(async () => {
    await deleteAllTodos();
    await loadTodos();
  }, [loadTodos]);

  return { todos, isLoading, error, addTodo, clearTodos };
}
