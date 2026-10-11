import api from './client';

export async function getIncidents(params = {}) {
  const { data } = await api.get('/incidents', { params });
  return data;
}

export async function getIncident(id) {
  return (await api.get(`/incidents/${id}`)).data;
}

export async function createIncident(payload) {
  return (await api.post('/incidents', payload)).data;
}

export async function updateIncident(id, payload) {
  return (await api.patch(`/incidents/${id}`, payload)).data;
}

export async function getIncidentAssignees(id) {
  return (await api.get(`/incidents/${id}/assignees`)).data;
}

export async function assignIncidentUser(id, userId) {
  return (
    await api.post(`/incidents/${id}/assignees`, {
      user_id: userId,
    })
  ).data;
}

export async function unassignIncidentUser(id, userId) {
  return (
    await api.delete(`/incidents/${id}/assignees/${userId}`)
  ).data;
}