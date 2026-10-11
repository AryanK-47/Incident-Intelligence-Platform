import api from './client';

export async function getUsers() {
  return (await api.get('/users/')).data;
}