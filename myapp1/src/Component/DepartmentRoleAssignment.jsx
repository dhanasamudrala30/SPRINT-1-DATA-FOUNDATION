import React from 'react';
import '../styles/DepartmentRoleAssignment.css';
import { useNavigate } from 'react-router-dom';

const DepartmentRoleAssignment = () => {
  const navigate = useNavigate();

  return (
    <div className="department-role-container">
      {/* Back Button */}
      <button className="back-btn" onClick={() => navigate('/dashboard1')}>
        ← Back
      </button>

      <h1>Department & Role Assignment</h1>

      <table className="department-role-table">
        <thead>
          <tr>
            <th>Department</th>
            <th>Designation</th>
            <th>Reporting Manager</th>
            <th>Lead</th>
            <th>Effective Date</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td>IT</td>
            <td>Software Engineer</td>
            <td>Mr. Rajesh Kumar</td>
            <td>Ms. Priya Sharma</td>
            <td>2022-08-15</td>
          </tr>
          <tr>
            <td>Chat Process</td>
            <td>Chat Support Executive</td>
            <td>Ms. Anjali Verma</td>
            <td>Mr. Sameer Singh</td>
            <td>2023-01-10</td>
          </tr>
        </tbody>
      </table>
    </div>
  );
};

export default DepartmentRoleAssignment;
