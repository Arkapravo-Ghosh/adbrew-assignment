export function TodoList({ todos, isLoading, error }) {
  if (isLoading && todos.length === 0) return <p>Loading…</p>;
  if (error) return <p role="alert" className="error">{error}</p>;
  if (todos.length === 0) return <p>No TODOs yet. Add one below!</p>;

  return (
    <ol className="todo-list">
      {todos.map((todo) => (
        <li key={todo.id}>{todo.description}</li>
      ))}
    </ol>
  );
}
