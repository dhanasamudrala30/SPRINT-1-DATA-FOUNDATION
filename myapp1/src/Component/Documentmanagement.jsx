import React from 'react';
import '../styles/DocumentManagement.css';
import { useNavigate } from 'react-router-dom';

const DocumentManagement = () => {
    const navigate = useNavigate();

    return (
        <div className="document-management-container">
            {/* Back Button */}
            <button className="back-btn" onClick={() => navigate('/dashboard1')}>
                ← Back
            </button>

            <h1>Document Management</h1>
            
            <table className="document-table">
                <thead>
                    <tr>
                        <th>Document Type</th>
                        <th>Document No.</th>
                        <th>Upload Date</th>
                        <th>Expiry Date</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td>SSC</td>
                        <td>SSC123456</td>
                        <td>2022-07-10</td>
                        <td>2032-07-09</td>
                    </tr>
                    <tr>
                        <td>Inter</td>
                        <td>INT654321</td>
                        <td>2020-05-15</td>
                        <td>2030-05-14</td>
                    </tr>
                    <tr>
                        <td>Graduation</td>
                        <td>GRAD987654</td>
                        <td>2018-06-01</td>
                        <td>2028-05-31</td>
                    </tr>
                    <tr>
                        <td>Aadhaar</td>
                        <td>1234-5678-9012</td>
                        <td>2019-01-10</td>
                        <td>2039-01-09</td>
                    </tr>
                    <tr>
                        <td>PAN</td>
                        <td>ABCDE1234F</td>
                        <td>2019-01-10</td>
                        <td>2029-01-09</td>
                    </tr>
                </tbody>
            </table>

        </div>
    );
};

export default DocumentManagement;
