import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import '../styles/Dashboard.css';
import logo from '../assets/companylogo.png';

const Dashboard = () => {
    const [isDropupOpen, setIsDropupOpen] = useState(false);
    const [sidebarOpen, setSidebarOpen] = useState(false);
    const navigate = useNavigate();

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
                {/* Sidebar */}
                <aside className={`sidebar ${sidebarOpen ? 'show' : ''}`}>
                    <div className="logo">
                        <img src={logo} alt="Logo" />
                        <h2>RMI Coders Hub</h2>
                    </div>

                    <nav className="nav-menu">
                        <a href="#" onClick={() => navigate('/dashboard1')}>
                            Employee Management
                        </a>
                        <a href="#" onClick={() => navigate('/dashboard2')}>
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

                {/* Centered Image + Text */}
                <div className="center-image">
                    <img
                        src="https://res.cloudinary.com/ds7dqfb1n/image/upload/v1759825337/rm1_coders_hub_software_solutions_logo_vkmki0.jpg"
                        alt="Company Logo"
                    />
                    <h2>RM1 CODER HUB SOFTWARE SOLUTIONS</h2>
                </div>
            </div>
        </>
    );
};

export default Dashboard;
