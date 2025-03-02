import api from '../../api/axios'

export const authService = {

  async register(userData) {
    try {
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


  async logout() {
    return api.post('/user/logout/');
  },

  async verify(){
    return api.post('/user/token/verify/');
  },

  async refreshToken(){
    return api.post('/user/token/refresh/');
  }
};