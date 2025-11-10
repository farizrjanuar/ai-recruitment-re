import React, { useState, useEffect } from 'react';
import { useParams, Link, useNavigate } from 'react-router-dom';
import jobAPI from '../services/jobAPI';
import './JobDetail.css';

const JobDetail = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const [job, setJob] = useState(null);
  const [candidates, setCandidates] = useState([]);
  const [loading, setLoading] = useState(true);
  const [loadingCandidates, setLoadingCandidates] = useState(false);
  const [error, setError] = useState('');
  const [minScore, setMinScore] = useState(0);
  const [statusFilter, setStatusFilter] = useState('all');

  useEffect(() => {
    fetchJob();
  }, [id]);

  useEffect(() => {
    if (job) {
      fetchCandidates();
    }
  }, [minScore, statusFilter]);

  const fetchJob = async () => {
    setLoading(true);
    setError('');
    
    try {
      const data = await jobAPI.getJobById(id);
      setJob(data);
      fetchCandidates();
    } catch (err) {
      setError(err.message || 'Failed to load job details');
    } finally {
      setLoading(false);
    }
  };

  const fetchCandidates = async () => {
    setLoadingCandidates(true);
    try {
      const data = await jobAPI.getJobCandidates(id, {
        min_score: minScore,
        status: statusFilter,
      });
      setCandidates(data.candidates || []);
    } catch (err) {
      console.error('Failed to load candidates:', err);
    } finally {
      setLoadingCandidates(false);
    }
  };

  const getMatchScoreColor = (score) => {
    if (score >= 80) return '#4caf50';
    if (score >= 60) return '#ff9800';
    return '#f44336';
  };

  const getQualificationBadge = (status) => {
    const statusClasses = {
      'Qualified': 'qualification-qualified',
      'Potentially Qualified': 'qualification-potential',
      'Not Qualified': 'qualification-not',
    };
    
    return (
      <span className={`qualification-badge ${statusClasses[status] || ''}`}>
        {status}
      </span>
    );
  };

  if (loading) {
    return <div className="loading">Loading job details...</div>;
  }

  if (error) {
    return (
      <div className="error-container">
        <div className="error-message">{error}</div>
        <Link to="/jobs" className="btn-back">
          Back to Jobs
        </Link>
      </div>
    );
  }

  if (!job) {
    return (
      <div className="error-container">
        <p>Job not found</p>
        <Link to="/jobs" className="btn-back">
          Back to Jobs
        </Link>
      </div>
    );
  }

  return (
    <div className="job-detail-container">
      <div className="detail-header">
        <Link to="/jobs" className="btn-back">
          ← Back to Jobs
        </Link>
        <div className="header-actions">
          <Link to={`/jobs/${id}/edit`} className="btn-edit">
            Edit Job
          </Link>
        </div>
      </div>

      <div className="job-detail-card">
        <div className="job-header">
          <div>
            <h2>{job.title}</h2>
            <span className={`job-status ${job.is_active ? 'active' : 'inactive'}`}>
              {job.is_active ? 'Active' : 'Inactive'}
            </span>
          </div>
        </div>

        <div className="job-section">
          <h3>Description</h3>
          <p className="job-description">{job.description || 'No description provided'}</p>
        </div>

        <div className="job-requirements">
          <div className="requirement-section">
            <h3>Required Skills</h3>
            <div className="skills-list">
              {job.required_skills && job.required_skills.length > 0 ? (
                job.required_skills.map((skill, index) => (
                  <span key={index} className="skill-tag required">
                    {skill}
                  </span>
                ))
              ) : (
                <p className="no-data-text">No required skills specified</p>
              )}
            </div>
          </div>

          <div className="requirement-section">
            <h3>Preferred Skills</h3>
            <div className="skills-list">
              {job.preferred_skills && job.preferred_skills.length > 0 ? (
                job.preferred_skills.map((skill, index) => (
                  <span key={index} className="skill-tag preferred">
                    {skill}
                  </span>
                ))
              ) : (
                <p className="no-data-text">No preferred skills specified</p>
              )}
            </div>
          </div>
        </div>

        <div className="job-info-grid">
          <div className="info-item">
            <span className="info-label">Minimum Experience:</span>
            <span className="info-value">{job.min_experience_years || 0} years</span>
          </div>
          <div className="info-item">
            <span className="info-label">Education Level:</span>
            <span className="info-value">{job.education_level || 'Not specified'}</span>
          </div>
          <div className="info-item">
            <span className="info-label">Created:</span>
            <span className="info-value">
              {job.created_at ? new Date(job.created_at).toLocaleDateString() : 'N/A'}
            </span>
          </div>
        </div>
      </div>

      <div className="candidates-section">
        <h3>Matched Candidates</h3>
        
        <div className="candidates-filters">
          <div className="filter-group">
            <label htmlFor="min-score">Minimum Score:</label>
            <input
              type="range"
              id="min-score"
              min="0"
              max="100"
              value={minScore}
              onChange={(e) => setMinScore(parseInt(e.target.value))}
            />
            <span className="score-value">{minScore}</span>
          </div>
          
          <div className="filter-group">
            <label htmlFor="status-filter">Status:</label>
            <select
              id="status-filter"
              value={statusFilter}
              onChange={(e) => setStatusFilter(e.target.value)}
            >
              <option value="all">All</option>
              <option value="Qualified">Qualified</option>
              <option value="Potentially Qualified">Potentially Qualified</option>
              <option value="Not Qualified">Not Qualified</option>
            </select>
          </div>
        </div>

        {loadingCandidates ? (
          <div className="loading-text">Loading candidates...</div>
        ) : candidates.length === 0 ? (
          <div className="no-candidates">
            <p>No candidates match the current filters.</p>
          </div>
        ) : (
          <div className="candidates-list">
            {candidates.map((candidate, index) => (
              <div key={index} className="candidate-card">
                <div className="candidate-header">
                  <div>
                    <Link to={`/candidates/${candidate.candidate_id}`} className="candidate-name">
                      {candidate.name || 'Unknown'}
                    </Link>
                    {getQualificationBadge(candidate.status)}
                  </div>
                  <div
                    className="match-score-circle"
                    style={{ background: getMatchScoreColor(candidate.match_score) }}
                  >
                    {Math.round(candidate.match_score)}
                  </div>
                </div>
                
                <div className="candidate-breakdown">
                  <div className="breakdown-item">
                    <span className="breakdown-label">Skills:</span>
                    <span className="breakdown-value">
                      {Math.round(candidate.breakdown?.skill_match || 0)}
                    </span>
                  </div>
                  <div className="breakdown-item">
                    <span className="breakdown-label">Experience:</span>
                    <span className="breakdown-value">
                      {Math.round(candidate.breakdown?.experience_match || 0)}
                    </span>
                  </div>
                  <div className="breakdown-item">
                    <span className="breakdown-label">Education:</span>
                    <span className="breakdown-value">
                      {Math.round(candidate.breakdown?.education_match || 0)}
                    </span>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

export default JobDetail;
