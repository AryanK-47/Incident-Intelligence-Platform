import axios from 'axios';

const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000',
  timeout: 12000,
  headers: { 'Content-Type': 'application/json' },
});

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token');
  if (token) config.headers.Authorization = `Bearer ${token}`;
  return config;
});

api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Don't redirect from login itself; let the page display the server message.
      localStorage.removeItem('access_token');
    }
    return Promise.reject(error);
  },
);

export const errorMessage = (error) => {
  const detail = error?.response?.data?.detail;
  if (Array.isArray(detail)) return detail.map((x) => x.msg).join(', ');
  if (typeof detail === 'string') return detail;
  if (error?.code === 'ERR_NETWORK') return 'Backend se connection nahi ho pa raha. API URL aur backend status check karo.';
  return error?.message || 'Something went wrong.';
};
export default api;
