// src/api/axios.js
import axios from 'axios';

// Create a base axios instance
const api = axios.create({
  baseURL: 'https://mahmoud1234.pythonanywhere.com/api',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
    'Accept': 'application/json'
  },
  // This is important for cookies
  withCredentials: true
});

// Response interceptor for handling errors
api.interceptors.response.use(
  (response) => {
    return response;
  },
  (error) => {
    console.error('API Error:', error.response?.data || error.message);
    return Promise.reject(error);
  }
);

export default api;