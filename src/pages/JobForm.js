import React, { useState, useEffect } from 'react';
import { useNavigate, useParams, Link } from 'react-router-dom';
import jobAPI from '../services/jobAPI';
import './JobForm.css';

const JobForm = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const isEditMode = !!id;

  const [formData, setFormData] = useState({
    title: '',
    description: '',
    required_skills: '',
    preferred_skills: '',
    min_experience_years: 0,
    education_level: '',
  });
  
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [fetchingJob, setFetchingJob] = useState(isEditMode);

  useEffect(() => {
    if (isEditMode) {
      fetchJob();
    }
  }, [id]);

  const fetchJob = async () => {
    setFetchingJob(true);
    try {
      const job = await jobAPI.getJobById(id);
      setFormData({
        title: job.title || '',
        description: job.description || '',
        required_skills: Array.isArray(job.required_skills) 
          ? job.required_skills.join(', ') 
          : '',
        preferred_skills: Array.isArray(job.preferred_skills) 
          ? job.preferred_skills.join(', ') 
          : '',
        min_experience_years: job.min_experience_years || 0,
        education_level: job.education_level || '',
      });
    } catch (err) {
      setError(err.message || 'Failed to load job details');
    } finally {
      setFetchingJob(false);
    }
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value,
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      // Convert comma-separated strings to arrays
      const jobData = {
        title: formData.title.trim(),
        description: formData.description.trim(),
        required_skills: formData.required_skills
          .split(',')
          .map(s => s.trim())
          .filter(s => s),
        preferred_skills: formData.preferred_skills
          .split(',')
          .map(s => s.trim())
          .filter(s => s),
        min_experience_years: parseInt(formData.min_experience_years) || 0,
        education_level: formData.education_level.trim(),
      };

      if (isEditMode) {
        await jobAPI.updateJob(id, jobData);
      } else {
        await jobAPI.createJob(jobData);
      }

      navigate('/jobs');
    } catch (err) {
      setError(err.message || `Failed to ${isEditMode ? 'update' : 'create'} job`);
    } finally {
      setLoading(false);
    }
  };

  if (fetchingJob) {
    return <div className="loading">Loading job details...</div>;
  }

  return (
    <div className="job-form-container">
      <div className="job-form-card">
        <div className="form-header">
          <Link to="/jobs" className="btn-back">
            ← Back to Jobs
          </Link>
          <h2>{isEditMode ? 'Edit Job Position' : 'Create New Job Position'}</h2>
        </div>

        {error && <div className="error-message">{error}</div>}

        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label htmlFor="title">Job Title *</label>
            <input
              type="text"
              id="title"
              name="title"
              value={formData.title}
              onChange={handleChange}
              required
              placeholder="e.g., Senior Software Engineer"
            />
          </div>

          <div className="form-group">
            <label htmlFor="description">Job Description *</label>
            <textarea
              id="description"
              name="description"
              value={formData.description}
              onChange={handleChange}
              required
              rows="6"
              placeholder="Describe the job role, responsibilities, and requirements..."
            />
          </div>

          <div className="form-group">
            <label htmlFor="required_skills">Required Skills *</label>
            <input
              type="text"
              id="required_skills"
              name="required_skills"
              value={formData.required_skills}
              onChange={handleChange}
              required
              placeholder="e.g., Python, React, SQL (comma-separated)"
            />
            <small className="form-hint">Enter skills separated by commas</small>
          </div>

          <div className="form-group">
            <label htmlFor="preferred_skills">Preferred Skills</label>
            <input
              type="text"
              id="preferred_skills"
              name="preferred_skills"
              value={formData.preferred_skills}
              onChange={handleChange}
              placeholder="e.g., Docker, AWS, Kubernetes (comma-separated)"
            />
            <small className="form-hint">Enter skills separated by commas</small>
          </div>

          <div className="form-row">
            <div className="form-group">
              <label htmlFor="min_experience_years">Minimum Experience (years)</label>
              <input
                type="number"
                id="min_experience_years"
                name="min_experience_years"
                value={formData.min_experience_years}
                onChange={handleChange}
                min="0"
                max="50"
              />
            </div>

            <div className="form-group">
              <label htmlFor="education_level">Education Level</label>
              <select
                id="education_level"
                name="education_level"
                value={formData.education_level}
                onChange={handleChange}
              >
                <option value="">Not specified</option>
                <option value="High School">High School</option>
                <option value="Associate">Associate Degree</option>
                <option value="Bachelor">Bachelor's Degree</option>
                <option value="Master">Master's Degree</option>
                <option value="PhD">PhD</option>
              </select>
            </div>
          </div>

          <div className="form-actions">
            <button
              type="button"
              onClick={() => navigate('/jobs')}
              className="btn-cancel"
              disabled={loading}
            >
              Cancel
            </button>
            <button
              type="submit"
              className="btn-submit"
              disabled={loading}
            >
              {loading 
                ? (isEditMode ? 'Updating...' : 'Creating...') 
                : (isEditMode ? 'Update Job' : 'Create Job')}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default JobForm;
