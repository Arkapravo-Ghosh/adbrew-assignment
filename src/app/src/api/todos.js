import { request } from './client';

export function fetchTodos({ signal } = {}) {
  return request('/todos', { signal });
}

export function createTodo(description) {
  return request('/todos', { method: 'POST', body: { description } });
}

export function deleteAllTodos() {
  return request('/todos', { method: 'DELETE' });
}
