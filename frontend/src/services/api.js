import axios from 'axios';

const API_BASE_URL = 'http://127.0.0.1:5000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json'
  }
});

// Add auth headers if token exists
api.interceptors.request.use(config => {
  const token = localStorage.getItem('auth_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Auth endpoints
export const authAPI = {
  register: (data) => api.post('/auth/register', data),
  login: (data) => api.post('/auth/login', data),
  adminLogin: (email, password) => 
    api.post('/admin/dashboard', {}, {
      headers: {
        'X-Admin-Email': email,
        'X-Admin-Password': password
      }
    })
};

// User endpoints
export const userAPI = {
  dashboard: (userId) => api.get(`/user/dashboard/${userId}`),
  parkVehicle: (data) => api.post('/user/park', data),
  unparkVehicle: (vehicleId) => api.patch(`/user/unpark/${vehicleId}`),
  history: (userId) => api.get(`/user/history/${userId}`),
  summary: (userId) => api.get(`/user/summary/${userId}`),
  exportHistory: (userId) => api.get(`/user/export/history/${userId}`),
  exportStatus: (taskId) => api.get(`/user/export/status/${taskId}`),
  downloadExport: (taskId) => api.get(`/user/export/result/${taskId}`)
};

// Admin endpoints
export const adminAPI = {
  dashboard: (email, password) => 
    api.get('/admin/dashboard', {
      headers: {
        'X-Admin-Email': email,
        'X-Admin-Password': password
      }
    }),
  createLot: (data, email, password) =>
    api.post('/admin/create_lot', data, {
      headers: {
        'X-Admin-Email': email,
        'X-Admin-Password': password
      }
    }),
  getLots: (email, password) =>
    api.get('/admin/lots', {
      headers: {
        'X-Admin-Email': email,
        'X-Admin-Password': password
      }
    }),
  getLot: (lotId, email, password) =>
    api.get(`/admin/lot/${lotId}`, {
      headers: {
        'X-Admin-Email': email,
        'X-Admin-Password': password
      }
    }),
  updateLot: (lotId, data, email, password) =>
    api.put(`/admin/lot/${lotId}`, data, {
      headers: {
        'X-Admin-Email': email,
        'X-Admin-Password': password
      }
    }),
  deleteLot: (lotId, email, password) =>
    api.delete(`/admin/lot/${lotId}`, {
      headers: {
        'X-Admin-Email': email,
        'X-Admin-Password': password
      }
    }),
  getParked: (email, password) =>
    api.get('/admin/parked', {
      headers: {
        'X-Admin-Email': email,
        'X-Admin-Password': password
      }
    })
};

export default api;