import React, { useState } from 'react';
import '../styles/Dashboard.css';
import logo from '../assets/companylogo.png'; // Logo path
import { useNavigate } from 'react-router-dom';

const Dashboard = () => {
  const [isDropupOpen, setIsDropupOpen] = useState(false);
  const navigate = useNavigate();

  const toggleDropup = () => {
    setIsDropupOpen(!isDropupOpen);
  };

  return (
    <div className="dashboard-container">
      <aside className="sidebar">
        <div className="logo">
          <img src={logo} alt="Logo" />
          <h2>RMI Coders Hub Software Solutions</h2>
        </div>

        <nav className="nav-menu">
          <a href="#" onClick={(e) => { e.preventDefault(); navigate('/dashboard1'); }}>
            Employee Management
          </a>
          <a href="#" onClick={(e) => { e.preventDefault(); navigate('/dashboard2'); }}>
            Leave & Attendance
          </a>
          <a href="#">Settings</a>
        </nav>

        <div className="admin-section">
          <div className="admin-info" onClick={toggleDropup}>
            <div className="admin-avatar">👤</div>
            <div>
              <p>User</p>
            </div>
          </div>

          {isDropupOpen && (
            <div className="dropup-menu">
              <ul>
                <li>My Profile</li>
                <li onClick={() => navigate('/login')}>Logout</li>
              </ul>
            </div>
          )}
        </div>
      </aside>

      <main className="main-content">
        {/* ⬅️ Back button added here */}
        <button className="back-btn" onClick={() => navigate('/dashboard')}>
          ← Back
        </button>

        <h1>Employee Management</h1>
        <p className="subheading">Comprehensive employee information and records</p>

        <div className="card-grid">
          <div className="card blue" onClick={() => navigate('/employee-profile')}>
            <div className="card-icon">👤</div>
            <h3>Employee Profile</h3>
            <p>View and manage employee ID, name, department, email, joining date, and contact information</p>
          </div>

          <div className="card green" onClick={() => navigate('/document-management')}>
            <div className="card-icon">📄</div>
            <h3>Document Management</h3>
            <p>Manage SSC, Inter, Graduation, Aadhaar, PAN, and other important documents</p>
          </div>

          <div className="card orange"onClick={() => navigate('/employee-directory')}>
            <div className="card-icon">📘</div>
            <h3>Employee Directory</h3>
            <p>Access employee ID, name, designation, and office email information</p>
          </div>

          <div className="card purple"onClick={() => navigate('/department-role-assignment')}>
            <div className="card-icon">🏢</div>
            <h3>Department & Role Assignment</h3>
            <p>Manage department assignments, designations, reporting managers, and team leads</p>
          </div>
        </div>
      </main>
    </div>
  );
};

export default Dashboard;
