import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import '../styles/Dashboard2.css';
import logo from '../assets/companylogo.png';

const Dashboard2 = () => {
  const navigate = useNavigate();
  const [isDropupOpen, setIsDropupOpen] = useState(false);
  const [sidebarOpen, setSidebarOpen] = useState(false);

  const toggleDropup = () => setIsDropupOpen(!isDropupOpen);
  const toggleSidebar = () => setSidebarOpen(!sidebarOpen);

  return (
    <>
      {/* Mobile Menu Bar */}
      <div className="menu-bar">
        <img src={logo} alt="Logo" style={{ height: '40px' }} />
        <button onClick={toggleSidebar}>☰</button>
      </div>

      <div className="dashboard-container">
        <aside className={`sidebar ${sidebarOpen ? 'show' : ''}`}>
          <div className="logo">
            <img src={logo} alt="Logo" />
            <h2>RMI Coders Hub</h2>
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
              <div><p>User</p></div>
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
          <button className="back-btn" onClick={() => navigate('/dashboard')}>
            ← Back
          </button>
          <h1>Leave & Attendance</h1>
          <p className="subheading">Leave and Attendance tracking</p>

          <div className="card-grid">
            <div className="card blue" onClick={() => navigate('/attendance-tracking')}>
              <div className="card-icon">📊</div>
              <h3>Attendance Tracking</h3>
              <p>Monitor daily attendance, track working hours, and manage attendance records efficiently.</p>
            </div>

            <div className="card green" onClick={() => navigate('/shift-roster')}>
              <div className="card-icon">🗓️</div>
              <h3>Shift & Roster</h3>
              <p>Plan and organize employee shifts, manage rosters, and handle schedule changes seamlessly.</p>
            </div>

            <div className="card orange" onClick={() => navigate('/leavepolicy')}>
              <div className="card-icon">📜</div>
              <h3>Leave Policy</h3>
              <p>Define company leave rules, accruals, carry-forward policies, and leave categories.</p>
            </div>

            <div className="card purple">
              <div className="card-icon">🔁</div>
              <h3>Leave Workflow</h3>
              <p>Automate leave requests, approvals, and tracking with transparent workflows.</p>
            </div>

            <div className="card pink" onClick={() => navigate('/holiday-calendar')}>
              <div className="card-icon">📆</div>
              <h3>Holiday Calendar</h3>
              <p>Maintain a centralized list of holidays for all departments and branches.</p>
            </div>
          </div>
        </main>
      </div>
    </>
  );
};

export default Dashboard2;
