import React from 'react';
import { Link, useNavigate } from 'react-router-dom';

const Navbar = () => {
  const navigate = useNavigate();

  const handleLogout = () => {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    navigate('/login');
  };

  return (
    <nav className="navbar">
      <h1>Voice AI SaaS</h1>
      <div>
        <Link to="/" className="nav-link">Dashboard</Link>
        <Link to="/campaigns" className="nav-link">Campaigns</Link>
        <Link to="/calls" className="nav-link">Calls</Link>
        <Link to="/analytics" className="nav-link">Analytics</Link>
        <button onClick={handleLogout} className="logout-btn">Logout</button>
      </div>
    </nav>
  );
};

export default Navbar;
