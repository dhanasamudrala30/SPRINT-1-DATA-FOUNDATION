import React from 'react';
import '../styles/ShiftRoster.css';
import { useNavigate } from 'react-router-dom';

const ShiftRoster = () => {
  const navigate = useNavigate();

  return (
    <div className="shift-container">
      {/* Back Button */}
      <button className="back-btn" onClick={() => navigate('/dashboard2')}>
        ← Back
      </button>

      <h1>Shift & Roster</h1>
      
      <table className="shift-table">
        <thead>
          <tr>
            <th>Shift ID</th>
            <th>Employee ID</th>
            <th>Shift Type</th>
            <th>Start Time</th>
            <th>End Time</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td>SHIFT001</td>
            <td>EMP001</td>
            <td>Day</td>
            <td>09:00 AM</td>
            <td>06:00 PM</td>
          </tr>
          <tr>
            <td>SHIFT002</td>
            <td>EMP002</td>
            <td>Night</td>
            <td>08:00 PM</td>
            <td>03:00 AM</td>
          </tr>
        </tbody>
      </table>
    </div>
  );
};

export default ShiftRoster;
