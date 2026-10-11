// src/api/auth.js
import api from './client';

export async function login(credentials) {
  const email = credentials.email ?? credentials.username;

  const { data } = await api.post('/auth/login', {
    email: email.trim(),
    password: credentials.password,
  });

  if (!data?.access_token) {
    throw new Error('Login response mein access_token nahi mila.');
  }

  localStorage.setItem('access_token', data.access_token);
  localStorage.setItem('auth_user', JSON.stringify(data.user ?? {}));

  return data;
}

export function logout() {
  localStorage.removeItem('access_token');
  localStorage.removeItem('auth_user');
}

export const isAuthenticated = () =>
  Boolean(localStorage.getItem('access_token'));