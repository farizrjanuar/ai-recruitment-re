import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { Chart as ChartJS, ArcElement, CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend } from 'chart.js';
import { Pie, Bar } from 'react-chartjs-2';
import dashboardAPI from '../services/dashboardAPI';
import candidateAPI from '../services/candidateAPI';
import './Dashboard.css';

// Register Chart.js components
ChartJS.register(ArcElement, CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend);

const Dashboard = () => {
  const [stats, setStats] = useState(null);
  const [analytics, setAnalytics] = useState(null);
  const [recentCandidates, setRecentCandidates] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    fetchDashboardData();
  }, []);

  const fetchDashboardData = async () => {
    setLoading(true);
    setError('');
    
    try {
      const [statsData, analyticsData, candidatesData] = await Promise.all([
        dashboardAPI.getStatistics(),
        dashboardAPI.getAnalytics(),
        candidateAPI.getCandidates({ page: 1, limit: 5 }),
      ]);
      
      setStats(statsData);
      setAnalytics(analyticsData);
      setRecentCandidates(candidatesData.candidates || []);
    } catch (err) {
      setError(err.message || 'Failed to load dashboard data');
    } finally {
      setLoading(false);
    }
  };

  const getSkillDistributionData = () => {
    if (!analytics?.skill_distribution) return null;
    
    const skills = Object.entries(analytics.skill_distribution)
      .sort((a, b) => b[1] - a[1])
      .slice(0, 10);
    
    return {
      labels: skills.map(([skill]) => skill),
      datasets: [
        {
          label: 'Number of Candidates',
          data: skills.map(([, count]) => count),
          backgroundColor: [
            '#667eea', '#764ba2', '#f093fb', '#4facfe',
            '#43e97b', '#fa709a', '#fee140', '#30cfd0',
            '#a8edea', '#fed6e3',
          ],
        },
      ],
    };
  };

  const getExperienceDistributionData = () => {
    if (!analytics?.experience_distribution) return null;
    
    const ranges = ['0-2', '3-5', '6-10', '11-15', '16+'];
    const data = ranges.map(range => analytics.experience_distribution[range] || 0);
    
    return {
      labels: ranges.map(r => `${r} years`),
      datasets: [
        {
          label: 'Number of Candidates',
          data: data,
          backgroundColor: '#667eea',
        },
      ],
    };
  };

  const getMatchScoreDistributionData = () => {
    if (!analytics?.match_score_distribution) return null;
    
    const ranges = ['0-20', '21-40', '41-60', '61-80', '81-100'];
    const data = ranges.map(range => analytics.match_score_distribution[range] || 0);
    
    return {
      labels: ranges,
      datasets: [
        {
          label: 'Number of Matches',
          data: data,
          backgroundColor: [
            '#f44336', '#ff9800', '#ffc107', '#8bc34a', '#4caf50',
          ],
        },
      ],
    };
  };

  const chartOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        position: 'bottom',
      },
    },
  };

  if (loading) {
    return <div className="loading">Loading dashboard...</div>;
  }

  if (error) {
    return (
      <div className="error-container">
        <div className="error-message">{error}</div>
        <button onClick={fetchDashboardData} className="btn-retry">
          Retry
        </button>
      </div>
    );
  }

  return (
    <div className="dashboard-container">
      <h2>HR Dashboard</h2>

      {/* Statistics Cards */}
      <div className="stats-grid">
        <div className="stat-card">
          <div className="stat-icon">👥</div>
          <div className="stat-content">
            <div className="stat-value">{stats?.total_candidates || 0}</div>
            <div className="stat-label">Total Candidates</div>
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-icon">💼</div>
          <div className="stat-content">
            <div className="stat-value">{stats?.total_jobs || 0}</div>
            <div className="stat-label">Active Jobs</div>
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-icon">⭐</div>
          <div className="stat-content">
            <div className="stat-value">
              {stats?.avg_match_score ? Math.round(stats.avg_match_score) : 0}
            </div>
            <div className="stat-label">Avg Match Score</div>
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-icon">✓</div>
          <div className="stat-content">
            <div className="stat-value">{stats?.qualified_candidates || 0}</div>
            <div className="stat-label">Qualified Candidates</div>
          </div>
        </div>
      </div>

      {/* Charts Section */}
      <div className="charts-grid">
        {/* Skill Distribution */}
        <div className="chart-card">
          <h3>Top Skills Distribution</h3>
          <div className="chart-container">
            {getSkillDistributionData() ? (
              <Pie data={getSkillDistributionData()} options={chartOptions} />
            ) : (
              <p className="no-data-text">No skill data available</p>
            )}
          </div>
        </div>

        {/* Experience Distribution */}
        <div className="chart-card">
          <h3>Experience Level Distribution</h3>
          <div className="chart-container">
            {getExperienceDistributionData() ? (
              <Bar data={getExperienceDistributionData()} options={chartOptions} />
            ) : (
              <p className="no-data-text">No experience data available</p>
            )}
          </div>
        </div>

        {/* Match Score Distribution */}
        <div className="chart-card">
          <h3>Match Score Distribution</h3>
          <div className="chart-container">
            {getMatchScoreDistributionData() ? (
              <Bar data={getMatchScoreDistributionData()} options={chartOptions} />
            ) : (
              <p className="no-data-text">No match score data available</p>
            )}
          </div>
        </div>
      </div>

      {/* Recent Candidates */}
      <div className="recent-candidates-card">
        <div className="card-header">
          <h3>Recent Candidates</h3>
          <Link to="/candidates" className="view-all-link">
            View All →
          </Link>
        </div>
        
        {recentCandidates.length > 0 ? (
          <div className="candidates-table">
            <table>
              <thead>
                <tr>
                  <th>Name</th>
                  <th>Email</th>
                  <th>Skills</th>
                  <th>Experience</th>
                  <th>Status</th>
                  <th>Actions</th>
                </tr>
              </thead>
              <tbody>
                {recentCandidates.map((candidate) => (
                  <tr key={candidate.id}>
                    <td>{candidate.name || 'N/A'}</td>
                    <td>{candidate.email || 'N/A'}</td>
                    <td>
                      {candidate.skills && candidate.skills.length > 0
                        ? candidate.skills.slice(0, 2).join(', ') +
                          (candidate.skills.length > 2 ? '...' : '')
                        : 'N/A'}
                    </td>
                    <td>{candidate.experience_years || 0} years</td>
                    <td>
                      <span className={`status-badge status-${candidate.status}`}>
                        {candidate.status}
                      </span>
                    </td>
                    <td>
                      <Link to={`/candidates/${candidate.id}`} className="btn-view-small">
                        View
                      </Link>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        ) : (
          <p className="no-data-text">No recent candidates</p>
        )}
      </div>
    </div>
  );
};

export default Dashboard;
