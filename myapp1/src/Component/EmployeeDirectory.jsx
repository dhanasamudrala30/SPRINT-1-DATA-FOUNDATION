import React from 'react';
import '../styles/EmployeeDirectory.css';
import { useNavigate } from 'react-router-dom';

const EmployeeDirectory = () => {
    const navigate = useNavigate();

    return (
        <div className="employee-directory-container">
            {/* Back Button */}
            <button className="back-btn" onClick={() => navigate('/dashboard1')}>
                ← Back
            </button>

            <h1>Employee Directory</h1>
           

            <table className="employee-directory-table">
                <thead>
                    <tr>
                        <th>Employee ID</th>
                        <th>Name</th>
                        <th>Designation</th>
                        <th>Department</th>
                        <th>Office Mail</th>
                        <th>Status</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td>EMP001</td>
                        <td>John Doe</td>
                        <td>Software Engineer</td>
                        <td>IT</td>
                        <td>john.doe@rmicoders.com</td>
                        <td className="status active">Active</td>
                    </tr>
                    <tr>
                        <td>EMP002</td>
                        <td>Jane Smith</td>
                        <td>Chat Support Executive</td>
                        <td>Chat Process</td>
                        <td>jane.smith@rmicoders.com</td>
                        <td className="status inactive">Inactive</td>
                    </tr>
                    <tr>
                        <td>EMP003</td>
                        <td>Robert Brown</td>
                        <td>Voice Support Executive</td>
                        <td>Voice Process</td>
                        <td>robert.brown@rmicoders.com</td>
                        <td className="status yet-to-leave">Yet to leave</td>
                    </tr>
                </tbody>
            </table>
        </div>
    );
};

export default EmployeeDirectory;
