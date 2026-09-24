import { useState } from 'react';

import { MAX_DESCRIPTION_LENGTH } from '../config';

export function TodoForm({ onSubmit, onClear, canClear }) {
  const [description, setDescription] = useState('');
  const [pendingAction, setPendingAction] = useState(null);
  const [error, setError] = useState(null);
  const isBusy = pendingAction !== null;

  // Runs an async action with shared busy/error handling; resolves to whether it succeeded.
  const runAction = async (action, perform) => {
    setPendingAction(action);
    setError(null);
    try {
      await perform();
      return true;
    } catch (err) {
      setError(err.message);
      return false;
    } finally {
      setPendingAction(null);
    }
  };

  const handleSubmit = async (event) => {
    event.preventDefault();

    const trimmed = description.trim();
    if (!trimmed) {
      setError('Please enter a description.');
      return;
    }

    if (await runAction('add', () => onSubmit(trimmed))) {
      setDescription('');
    }
  };

  const handleClear = async () => {
    if (!window.confirm('Delete all TODOs? This cannot be undone.')) return;
    await runAction('clear', onClear);
  };

  return (
    <form onSubmit={handleSubmit} noValidate>
      <div>
        <label htmlFor="todo-description">ToDo: </label>
        <input
          id="todo-description"
          type="text"
          value={description}
          onChange={(event) => setDescription(event.target.value)}
          maxLength={MAX_DESCRIPTION_LENGTH}
          disabled={isBusy}
        />
      </div>
      {error && <p role="alert" className="error">{error}</p>}
      <div className="form-actions">
        <button type="submit" disabled={isBusy}>
          {pendingAction === 'add' ? 'Adding…' : 'Add ToDo!'}
        </button>
        <button type="button" onClick={handleClear} disabled={isBusy || !canClear}>
          {pendingAction === 'clear' ? 'Clearing…' : 'Clear list'}
        </button>
      </div>
    </form>
  );
}
