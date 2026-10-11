import api from './client';
export async function getAnalysis(id) { return (await api.get(`/incidents/${id}/ai-analysis`)).data; }
export async function createAnalysis(id, payload) { return (await api.post(`/incidents/${id}/ai-analysis`, payload)).data; }
export async function getAnalysisVersions(id) { return (await api.get(`/incidents/${id}/ai-analysis/versions`)).data; }
export async function getIncidentEvents(id) { return (await api.get(`/incidents/${id}/events`)).data; }
