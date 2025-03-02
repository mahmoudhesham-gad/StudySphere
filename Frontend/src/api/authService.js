import axios from 'axios';
import api from './axios';


const API_URL = 'https://mahmoud1234.pythonanywhere.com/api';

// Configure axios defaults
axios.defaults.withCredentials = true;
axios.defaults.headers.common['Content-Type'] = 'application/json';
axios.defaults.headers.common['Accept'] = 'application/json';

export const authService = {
  async register(userData) {
    try {
      console.log('Registering user:', userData); 
      const response = await api.post('/user/register/', userData);
      return response.data;
    } catch (error) {
      console.error('Registration error:', error.response || error);
      throw error;
    }
  },

  async login(credentials) {
    const response = await api.post('/user/login/', credentials);
    return response.data;
  },

  async getCurrentUser() {
    return api.get('/user/profile/');
  },

  async logout() {
    return api.post('/user/logout/');
  }
};