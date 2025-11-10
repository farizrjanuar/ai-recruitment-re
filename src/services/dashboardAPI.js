import api from './api';

// Dashboard API endpoints
const dashboardAPI = {
  // Get dashboard statistics
  getStatistics: async () => {
    const response = await api.get('/dashboard/stats');
    return response.data;
  },

  // Get dashboard analytics
  getAnalytics: async () => {
    const response = await api.get('/dashboard/analytics');
    return response.data;
  },
};

export default dashboardAPI;
