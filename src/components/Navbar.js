import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import './Navbar.css';

const Navbar = () => {
  const location = useLocation();

  const isActive = (path) => {
    return location.pathname === path || location.pathname.startsWith(path + '/');
  };

  return (
    <nav className="navbar">
      <div className="navbar-container">
        <Link to="/dashboard" className="navbar-brand">
          AI Recruitment System
        </Link>

        <div className="navbar-menu">
          <Link
            to="/dashboard"
            className={`nav-link ${isActive('/dashboard') ? 'active' : ''}`}
          >
            Dashboard
          </Link>
          <Link
            to="/candidates"
            className={`nav-link ${isActive('/candidates') ? 'active' : ''}`}
          >
            Candidates
          </Link>
          <Link
            to="/jobs"
            className={`nav-link ${isActive('/jobs') ? 'active' : ''}`}
          >
            Jobs
          </Link>
          <Link
            to="/upload"
            className={`nav-link ${isActive('/upload') ? 'active' : ''}`}
          >
            Upload CV
          </Link>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
