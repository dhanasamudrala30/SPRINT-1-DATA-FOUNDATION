import React from 'react';
import '../styles/LeavePolicy.css';
import logo from '../assets/companylogo.png';
import { useNavigate } from 'react-router-dom';

const LeavePolicy = () => {
    const navigate = useNavigate();

    return (
        
        <div className="policy-container">
            {/* Back Button */}
            <button className="back-btn" onClick={() => navigate('/dashboard2')}>
                ← Back
            </button>

            {/* Page 1 - Header & Structure */}
            <div className="policy-page">
                <div className="policy-header">
                    <img src={logo} alt="Company Logo" className="company-logo" />
                    <h2>RMI Coders Hub Software Solutions</h2>
                    <h3>LEAVE POLICY</h3>
                    <p className="note">
                        {`{This is a sample company policy. For state-wise leave rules, please refer to regional regulations.}`}
                    </p>
                </div>

                <h4>Purpose</h4>
                <p><strong>Effective Date:</strong> ____________</p>
                <p><strong>Leave Entitlement for the Year:</strong></p>
                <ul>
                    <li>30 Earned/Paid Leaves</li>
                    <li>12 Public Holidays</li>
                </ul>

                <h4>Salient Features:</h4>
                <ul className="terms-list">
                    <li>All employees must utilize five days of leave every calendar year.</li>
                    <li>Unused leaves lapse on December 31st each year.</li>
                    <li>Carried forward leaves are limited to 30 days.</li>
                    <li>Leave encashment allowed only on resignation or retirement.</li>
                    <li>Probation employees can avail sick leave based on management discretion.</li>
                    <li>Minimum of 5 consecutive working days must be taken annually.</li>
                    <li>All leaves require prior approval from supervisor and HR.</li>
                </ul>
            </div>

            {/* Page 2 */}
            <div className="policy-page">
                <h4>Additional Terms & Conditions</h4>
                <ul className="terms-list">
                    <li>Employees must inform their manager within 4 hours if they can’t attend work.</li>
                    <li>Medical certificate required for leaves longer than 3 days due to sickness.</li>
                    <li>Planned long leaves must be approved 2 weeks before the start date.</li>
                    <li>Leave encashment is only processed during final settlement.</li>
                    <li>Emergency leaves are subject to manager approval and documentation.</li>
                    <li>Unplanned absence will lead to deduction of leave or salary.</li>
                    <li>Notice period cannot be clubbed with paid leave.</li>
                </ul>

                <div className="sign-section">
                    <p><strong>Authorized By:</strong> HR Department</p>
                    <p><strong>Effective Date:</strong> January 1, 2025</p>
                </div>
            </div>
        </div>
    );
};

export default LeavePolicy;
