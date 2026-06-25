import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import "../styles/Login.css";
import loginImage from "../assets/login-image.jpg"; // your image

function Login() {
  const navigate = useNavigate();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  const handleLogin = (e) => {
    e.preventDefault();

    const storedEmail = localStorage.getItem("userEmail");
    const storedPassword = localStorage.getItem("userPassword");

    if (!storedEmail && !storedPassword) {
      localStorage.setItem("userEmail", email);
      localStorage.setItem("userPassword", password);
      setError("");
      navigate("/dashboard");
      return;
    }

    if (email === storedEmail && password === storedPassword) {
      setError("");
      navigate("/dashboard");
    } else if (email === storedEmail && password !== storedPassword) {
      setError("Incorrect password! Try again or reset it.");
    } else {
      localStorage.setItem("userEmail", email);
      localStorage.setItem("userPassword", password);
      setError("");
      navigate("/dashboard");
    }
  };

  return (
    <div className="login-page">
      <div className="login-container">
        {/* Left side: Image */}
        <div className="login-left">
          <img src={loginImage} alt="Login" />
        </div>

        {/* Right side: Form card */}
        <div className="login-right">
          <div className="login-card">
            <h2>Login</h2>
            <form onSubmit={handleLogin}>
              <input
                type="email"
                placeholder="Enter Email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
              />
              <input
                type="password"
                placeholder="Enter Password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
              />
              <button type="submit">Login</button>
              {error && <p className="error-message">{error}</p>}
              <p className="forgot-password">
                <span onClick={() => navigate("/reset-password")}>Forgot Password?</span>
              </p>
            </form>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Login;
