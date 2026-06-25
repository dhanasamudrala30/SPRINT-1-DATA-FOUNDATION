import React from 'react';
import '../styles/EmployeeProfile.css';
import { useNavigate } from 'react-router-dom';

const EmployeeProfile = () => {
  const navigate = useNavigate();

  return (
    <div className="employee-profile-container">
      {/* Back Button */}
      <button className="back-btn" onClick={() => navigate('/dashboard1')}>
        ← Back
      </button>

      <h1>Employee Profile</h1>
      

      <table className="employee-table">
        <thead>
          <tr>
            <th>Employee ID</th>
            <th>Name</th>
            <th>Department</th>
            <th>Email ID</th>
            <th>Joining Date</th>
            <th>Contact</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td>RM1001</td>
            <td>Dhana</td>
            <td>Software Engineering</td>
            <td>dhana@gmail.com</td>
            <td>2025-10-06</td>
            <td>+91 9876543210</td>
          </tr>
        </tbody>
      </table>
    </div>
  );
};

export default EmployeeProfile;
