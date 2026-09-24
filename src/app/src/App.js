import './App.css';
import { TodoForm } from './components/TodoForm';
import { TodoList } from './components/TodoList';
import { useTodos } from './hooks/useTodos';

export function App() {
  const { todos, isLoading, error, addTodo, clearTodos } = useTodos();

  return (
    <div className="App">
      <div>
        <h1>List of TODOs</h1>
        <TodoList todos={todos} isLoading={isLoading} error={error} />
      </div>
      <div>
        <h1>Create a ToDo</h1>
        <TodoForm onSubmit={addTodo} onClear={clearTodos} canClear={todos.length > 0} />
      </div>
    </div>
  );
}

export default App;
