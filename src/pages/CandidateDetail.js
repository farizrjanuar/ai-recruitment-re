import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import candidateAPI from '../services/candidateAPI';
import './CandidateDetail.css';

const CandidateDetail = () => {
  const { id } = useParams();
  const [candidate, setCandidate] = useState(null);
  const [matches, setMatches] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [loadingMatches, setLoadingMatches] = useState(false);

  useEffect(() => {
    fetchCandidate();
  }, [id]);

  const fetchCandidate = async () => {
    setLoading(true);
    setError('');
    
    try {
      const data = await candidateAPI.getCandidateById(id);
      setCandidate(data);
      
      // Fetch matches if candidate is completed
      if (data.status === 'completed') {
        fetchMatches();
      }
    } catch (err) {
      setError(err.message || 'Failed to load candidate details');
    } finally {
      setLoading(false);
    }
  };

  const fetchMatches = async () => {
    setLoadingMatches(true);
    try {
      const data = await candidateAPI.getCandidateMatches(id);
      setMatches(data.matches || []);
    } catch (err) {
      console.error('Failed to load matches:', err);
    } finally {
      setLoadingMatches(false);
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
    return <div className="loading">Loading candidate details...</div>;
  }

  if (error) {
    return (
      <div className="error-container">
        <div className="error-message">{error}</div>
        <Link to="/candidates" className="btn-back">
          Back to Candidates
        </Link>
      </div>
    );
  }

  if (!candidate) {
    return (
      <div className="error-container">
        <p>Candidate not found</p>
        <Link to="/candidates" className="btn-back">
          Back to Candidates
        </Link>
      </div>
    );
  }

  return (
    <div className="candidate-detail-container">
      <div className="detail-header">
        <Link to="/candidates" className="btn-back">
          ← Back to Candidates
        </Link>
        <h2>Candidate Profile</h2>
      </div>

      <div className="detail-grid">
        {/* Personal Information */}
        <div className="detail-card">
          <h3>Personal Information</h3>
          <div className="info-row">
            <span className="info-label">Name:</span>
            <span className="info-value">{candidate.name || 'N/A'}</span>
          </div>
          <div className="info-row">
            <span className="info-label">Email:</span>
            <span className="info-value">{candidate.email || 'N/A'}</span>
          </div>
          <div className="info-row">
            <span className="info-label">Phone:</span>
            <span className="info-value">{candidate.phone || 'N/A'}</span>
          </div>
          <div className="info-row">
            <span className="info-label">Total Experience:</span>
            <span className="info-value">
              {candidate.total_experience_years || 0} years
            </span>
          </div>
          <div className="info-row">
            <span className="info-label">Status:</span>
            <span className={`status-badge status-${candidate.status}`}>
              {candidate.status}
            </span>
          </div>
        </div>

        {/* Education */}
        <div className="detail-card">
          <h3>Education</h3>
          {candidate.education && candidate.education.length > 0 ? (
            <div className="education-list">
              {candidate.education.map((edu, index) => (
                <div key={index} className="education-item">
                  <div className="edu-degree">{edu.degree || 'Degree'}</div>
                  <div className="edu-institution">
                    {edu.institution || 'Institution'}
                  </div>
                  {edu.year && (
                    <div className="edu-year">Year: {edu.year}</div>
                  )}
                </div>
              ))}
            </div>
          ) : (
            <p className="no-data-text">No education information available</p>
          )}
        </div>

        {/* Skills */}
        <div className="detail-card full-width">
          <h3>Skills</h3>
          {candidate.skills && candidate.skills.length > 0 ? (
            <div className="skills-grid">
              {candidate.skills.map((skill, index) => (
                <div key={index} className="skill-item">
                  <div className="skill-name">
                    {typeof skill === 'string' ? skill : skill.name}
                  </div>
                  {typeof skill === 'object' && skill.category && (
                    <div className="skill-category">{skill.category}</div>
                  )}
                  {typeof skill === 'object' && skill.score && (
                    <div className="skill-score">
                      Score: {Math.round(skill.score)}
                    </div>
                  )}
                </div>
              ))}
            </div>
          ) : (
            <p className="no-data-text">No skills information available</p>
          )}
        </div>

        {/* Work Experience */}
        <div className="detail-card full-width">
          <h3>Work Experience</h3>
          {candidate.experience && candidate.experience.length > 0 ? (
            <div className="experience-list">
              {candidate.experience.map((exp, index) => (
                <div key={index} className="experience-item">
                  <div className="exp-title">{exp.title || 'Position'}</div>
                  <div className="exp-company">{exp.company || 'Company'}</div>
                  {exp.duration && (
                    <div className="exp-duration">{exp.duration}</div>
                  )}
                  {exp.description && (
                    <div className="exp-description">{exp.description}</div>
                  )}
                </div>
              ))}
            </div>
          ) : (
            <p className="no-data-text">No work experience information available</p>
          )}
        </div>

        {/* Certifications */}
        {candidate.certifications && candidate.certifications.length > 0 && (
          <div className="detail-card full-width">
            <h3>Certifications</h3>
            <div className="certifications-list">
              {candidate.certifications.map((cert, index) => (
                <div key={index} className="certification-item">
                  {cert}
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Job Matches */}
        <div className="detail-card full-width">
          <h3>Job Position Matches</h3>
          {loadingMatches ? (
            <p className="loading-text">Loading matches...</p>
          ) : matches.length > 0 ? (
            <div className="matches-list">
              {matches.map((match, index) => (
                <div key={index} className="match-item">
                  <div className="match-header">
                    <Link to={`/jobs/${match.job_id}`} className="match-title">
                      {match.job_title}
                    </Link>
                    {getQualificationBadge(match.status)}
                  </div>
                  <div className="match-scores">
                    <div className="score-item">
                      <div
                        className="score-circle"
                        style={{
                          background: getMatchScoreColor(match.match_score),
                        }}
                      >
                        {Math.round(match.match_score)}
                      </div>
                      <div className="score-label">Overall</div>
                    </div>
                    <div className="score-item">
                      <div className="score-value">
                        {Math.round(match.skill_match)}
                      </div>
                      <div className="score-label">Skills</div>
                    </div>
                    <div className="score-item">
                      <div className="score-value">
                        {Math.round(match.experience_match)}
                      </div>
                      <div className="score-label">Experience</div>
                    </div>
                    <div className="score-item">
                      <div className="score-value">
                        {Math.round(match.education_match)}
                      </div>
                      <div className="score-label">Education</div>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <p className="no-data-text">
              No job matches available. Matches will be calculated automatically.
            </p>
          )}
        </div>
      </div>
    </div>
  );
};

export default CandidateDetail;
