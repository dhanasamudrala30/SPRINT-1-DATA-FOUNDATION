import React, { useState } from "react";
import { Link } from "react-router-dom";
import "./../styles/ResetPassword.css";

function ResetPassword() {
  const [newPassword, setNewPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [message, setMessage] = useState("");

  const handleReset = (e) => {
    e.preventDefault();

    // Validate password match
    if (newPassword !== confirmPassword) {
      setMessage("Passwords do not match!");
      return;
    }

    // Save new password
    localStorage.setItem("userPassword", newPassword);
    setMessage("Password reset successful!");
  };

  return (
    <div className="reset-page">
      <div className="reset-card">
        <h2>Reset Password</h2>
        <form onSubmit={handleReset}>
          <input
            type="password"
            placeholder="Enter new password"
            value={newPassword}
            onChange={(e) => setNewPassword(e.target.value)}
            required
          />
          <input
            type="password"
            placeholder="Confirm new password"
            value={confirmPassword}
            onChange={(e) => setConfirmPassword(e.target.value)}
            required
          />
          <button type="submit">Reset Password</button>
        </form>
        {message && <p className="success-message">{message}</p>}
        {/* Link to go back to login */}
        <p style={{ marginTop: "10px" }}>
          <Link to="/login">Back to Login</Link>
        </p>
      </div>
    </div>
  );
}

export default ResetPassword;