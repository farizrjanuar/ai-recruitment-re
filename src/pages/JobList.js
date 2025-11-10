import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import jobAPI from '../services/jobAPI';
import './JobList.css';

const JobList = () => {
  const [jobs, setJobs] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    fetchJobs();
  }, []);

  const fetchJobs = async () => {
    setLoading(true);
    setError('');
    
    try {
      const data = await jobAPI.getJobs();
      setJobs(data.jobs || []);
    } catch (err) {
      setError(err.message || 'Failed to load job positions');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="job-list-container">
      <div className="job-list-header">
        <h2>Job Positions</h2>
        <Link to="/jobs/new" className="btn-primary">
          Create New Job
        </Link>
      </div>

      {error && <div className="error-message">{error}</div>}

      {loading ? (
        <div className="loading">Loading job positions...</div>
      ) : jobs.length === 0 ? (
        <div className="no-data">
          <p>No job positions found.</p>
          <Link to="/jobs/new" className="btn-secondary">
            Create your first job position
          </Link>
        </div>
      ) : (
        <div className="jobs-grid">
          {jobs.map((job) => (
            <div key={job.id} className="job-card">
              <div className="job-card-header">
                <h3>{job.title}</h3>
                <span className={`job-status ${job.is_active ? 'active' : 'inactive'}`}>
                  {job.is_active ? 'Active' : 'Inactive'}
                </span>
              </div>
              
              <p className="job-description">
                {job.description && job.description.length > 150
                  ? job.description.substring(0, 150) + '...'
                  : job.description || 'No description'}
              </p>
              
              <div className="job-info">
                <div className="info-item">
                  <span className="info-label">Required Skills:</span>
                  <span className="info-value">
                    {job.required_skills && job.required_skills.length > 0
                      ? job.required_skills.slice(0, 3).join(', ') +
                        (job.required_skills.length > 3 ? '...' : '')
                      : 'None specified'}
                  </span>
                </div>
                
                <div className="info-item">
                  <span className="info-label">Min Experience:</span>
                  <span className="info-value">
                    {job.min_experience_years || 0} years
                  </span>
                </div>
                
                <div className="info-item">
                  <span className="info-label">Candidates:</span>
                  <span className="info-value">
                    {job.candidate_count || 0}
                  </span>
                </div>
                
                <div className="info-item">
                  <span className="info-label">Created:</span>
                  <span className="info-value">
                    {job.created_at
                      ? new Date(job.created_at).toLocaleDateString()
                      : 'N/A'}
                  </span>
                </div>
              </div>
              
              <div className="job-actions">
                <Link to={`/jobs/${job.id}`} className="btn-view">
                  View Details
                </Link>
                <Link to={`/jobs/${job.id}/edit`} className="btn-edit">
                  Edit
                </Link>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default JobList;
