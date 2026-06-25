import React from 'react';
import '../styles/AttendanceTracking.css';
import { useNavigate } from 'react-router-dom';

const AttendanceTracking = () => {
  const navigate = useNavigate();

  return (
    <div className="attendance-container">
      {/* Back Button */}
      <button className="back-btn" onClick={() => navigate('/dashboard2')}>
        ← Back
      </button>

      <h1>Attendance Tracking</h1>
      

      <table className="attendance-table">
        <thead>
          <tr>
            <th>Employee ID</th>
            <th>Date</th>
            <th>Status</th>
            <th>Check-In</th>
            <th>Check-Out</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td>EMP001</td>
            <td>2025-10-13</td>
            <td>Present</td>
            <td>10:00 AM</td>
            <td>07:00 PM</td>
          </tr>
        </tbody>
      </table>
    </div>
  );
};

export default AttendanceTracking;
