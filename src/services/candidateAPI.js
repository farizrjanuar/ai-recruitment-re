import api from './api';

// Candidate API endpoints
const candidateAPI = {
  // Upload CV file
  uploadCV: async (file, onUploadProgress) => {
    const formData = new FormData();
    formData.append('cv_file', file);

    const response = await api.post('/candidates/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
      onUploadProgress,
    });
    
    return response.data;
  },

  // Get all candidates with pagination and filters
  getCandidates: async (params = {}) => {
    const { page = 1, limit = 20, status, job_id } = params;
    
    const queryParams = new URLSearchParams({
      page: page.toString(),
      limit: limit.toString(),
    });
    
    if (status) queryParams.append('status', status);
    if (job_id) queryParams.append('job_id', job_id);
    
    const response = await api.get(`/candidates?${queryParams.toString()}`);
    return response.data;
  },

  // Get candidate by ID
  getCandidateById: async (candidateId) => {
    const response = await api.get(`/candidates/${candidateId}`);
    return response.data;
  },

  // Get candidate match results
  getCandidateMatches: async (candidateId) => {
    const response = await api.post(`/matching/calculate/${candidateId}`);
    return response.data;
  },

  // Delete candidate
  deleteCandidate: async (candidateId) => {
    const response = await api.delete(`/candidates/${candidateId}`);
    return response.data;
  },
};

export default candidateAPI;
