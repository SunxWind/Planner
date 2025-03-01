import axios from 'axios';
import { API_BASE_URL } from '../config.js';

export default {
  async login(username, password) {
    try {
      const response = await axios.post(`${API_BASE_URL}/token/`, { username, password });
      localStorage.setItem('token', response.data.access);
      localStorage.setItem('refresh', response.data.refresh);
      return response.data;
    } catch (error) {
      throw error.response.data;
    }
  },

  logout() {
    localStorage.removeItem('token');
    localStorage.removeItem('refresh');
  },

  getToken() {
    return localStorage.getItem('token');
  },

  isAuthenticated() {
    return !!localStorage.getItem('token');
  }
};