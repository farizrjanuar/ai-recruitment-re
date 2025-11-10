import api from './api';

// Job Position API endpoints
const jobAPI = {
  // Create a new job position
  createJob: async (jobData) => {
    const response = await api.post('/jobs', jobData);
    return response.data;
  },

  // Get all job positions
  getJobs: async () => {
    const response = await api.get('/jobs');
    return response.data;
  },

  // Get job by ID
  getJobById: async (jobId) => {
    const response = await api.get(`/jobs/${jobId}`);
    return response.data;
  },

  // Update job position
  updateJob: async (jobId, jobData) => {
    const response = await api.put(`/jobs/${jobId}`, jobData);
    return response.data;
  },

  // Get candidates matched to a job
  getJobCandidates: async (jobId, params = {}) => {
    const { min_score = 0, status = 'all' } = params;
    
    const queryParams = new URLSearchParams({
      min_score: min_score.toString(),
      status,
    });
    
    const response = await api.get(`/matching/job/${jobId}?${queryParams.toString()}`);
    return response.data;
  },
};

export default jobAPI;
