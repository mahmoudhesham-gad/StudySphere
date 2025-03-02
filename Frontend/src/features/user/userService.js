// src/api/userService.js
import api from '../../api/axios';

export const userService = {
  async getCurrentUser() {
    return api.get('/user/profile/');
  },
    async updateProfile(formData) {
    return api.patch('/user/profile/', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
  },
};