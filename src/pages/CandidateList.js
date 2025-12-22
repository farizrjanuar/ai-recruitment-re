import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import candidateAPI from '../services/candidateAPI';
import './CandidateList.css';

const CandidateList = () => {
  const [candidates, setCandidates] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [page, setPage] = useState(1);
  const [total, setTotal] = useState(0);
  const [statusFilter, setStatusFilter] = useState('');
  const limit = 20;

  useEffect(() => {
    fetchCandidates();
  }, [page, statusFilter]);

  const fetchCandidates = async () => {
    setLoading(true);
    setError('');
    
    try {
      const params = { page, limit };
      if (statusFilter) {
        params.status = statusFilter;
      }
      
      const data = await candidateAPI.getCandidates(params);
      setCandidates(data.candidates || []);
      setTotal(data.total || 0);
    } catch (err) {
      setError(err.message || 'Failed to load candidates');
    } finally {
      setLoading(false);
    }
  };

  const handleDeleteCandidate = async (candidateId, candidateName) => {
    if (!window.confirm(`Are you sure you want to delete "${candidateName}"? This action cannot be undone.`)) {
      return;
    }

    try {
      await candidateAPI.deleteCandidate(candidateId);
      // Refresh the candidate list
      fetchCandidates();
    } catch (err) {
      setError(err.message || 'Failed to delete candidate');
    }
  };

  const totalPages = Math.ceil(total / limit);

  const getStatusBadge = (status) => {
    const statusClasses = {
      completed: 'status-completed',
      processing: 'status-processing',
      failed: 'status-failed',
    };
    
    return (
      <span className={`status-badge ${statusClasses[status] || ''}`}>
        {status}
      </span>
    );
  };

  return (
    <div className="candidate-list-container">
      <div className="candidate-list-header">
        <h2>Candidates</h2>
        <Link to="/upload" className="btn-primary">
          Upload New CV
        </Link>
      </div>

      <div className="filters">
        <label htmlFor="status-filter">Filter by Status:</label>
        <select
          id="status-filter"
          value={statusFilter}
          onChange={(e) => {
            setStatusFilter(e.target.value);
            setPage(1);
          }}
        >
          <option value="">All</option>
          <option value="completed">Completed</option>
          <option value="processing">Processing</option>
          <option value="failed">Failed</option>
        </select>
      </div>

      {error && <div className="error-message">{error}</div>}

      {loading ? (
        <div className="loading">Loading candidates...</div>
      ) : candidates.length === 0 ? (
        <div className="no-data">
          <p>No candidates found.</p>
          <Link to="/upload" className="btn-secondary">
            Upload your first CV
          </Link>
        </div>
      ) : (
        <>
          <div className="candidate-table">
            <table>
              <thead>
                <tr>
                  <th>Name</th>
                  <th>Email</th>
                  <th>Skills</th>
                  <th>Experience</th>
                  <th>Status</th>
                  <th>Date Added</th>
                  <th>Actions</th>
                </tr>
              </thead>
              <tbody>
                {candidates.map((candidate) => (
                  <tr key={candidate.id}>
                    <td>{candidate.name || 'N/A'}</td>
                    <td>{candidate.email || 'N/A'}</td>
                    <td>
                      <div className="skills-preview">
                        {candidate.skills && candidate.skills.length > 0
                          ? candidate.skills
                              .slice(0, 3)
                              .map(skill => typeof skill === 'object' ? skill.name : skill)
                              .join(', ') +
                            (candidate.skills.length > 3 ? '...' : '')
                          : 'N/A'}
                      </div>
                    </td>
                    <td>{candidate.total_experience_years || 0} years</td>
                    <td>{getStatusBadge(candidate.status)}</td>
                    <td>
                      {candidate.created_at
                        ? new Date(candidate.created_at).toLocaleDateString()
                        : 'N/A'}
                    </td>
                    <td>
                      <Link
                        to={`/candidates/${candidate.id}`}
                        className="btn-view"
                      >
                        View
                      </Link>
                      <button
                        onClick={() => handleDeleteCandidate(candidate.id, candidate.name)}
                        className="btn-delete"
                        style={{ marginLeft: '8px' }}
                      >
                        Delete
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          {totalPages > 1 && (
            <div className="pagination">
              <button
                onClick={() => setPage(page - 1)}
                disabled={page === 1}
                className="btn-page"
              >
                Previous
              </button>
              <span className="page-info">
                Page {page} of {totalPages} ({total} total)
              </span>
              <button
                onClick={() => setPage(page + 1)}
                disabled={page === totalPages}
                className="btn-page"
              >
                Next
              </button>
            </div>
          )}
        </>
      )}
    </div>
  );
};

export default CandidateList;
