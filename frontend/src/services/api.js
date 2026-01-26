
import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:5000/api', // Flask Backend URL
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request Interceptor: Add JWT to headers
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers['Authorization'] = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Response Interceptor: Handle 401 (Unauthorized)
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response && error.response.status === 401) {
      console.warn("API INTERCEPTOR: 401 Unauthorized detected. Redirecting to login.");
      localStorage.removeItem('token');
      localStorage.removeItem('user');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

export default api;
