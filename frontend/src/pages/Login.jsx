import React, { useState } from "react";
import "../assets/styles/Login.css";
import { handleLogin } from "../assets/scripts/Login.js"; // we already wrote handleLogin
import { useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

const Login = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");
  const { login } = useAuth();
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setSuccess("");

    const result = await handleLogin(email, password);

    if (result.success) {
      setSuccess("✅ Login successful! Redirecting...");
        // Log user in via AuthContext
        login({ email, name: result.user?.name, occupation: result.user?.occupation });
      console.log("User:", result.user);
      // ✅ Redirect to home page after 1s
      setTimeout(() => {
        navigate("/");
      }, 1000);

      // ✅ Redirect to home page
      setTimeout(() => {
        window.location.href = "/";
      }, 1500);
    } else {
      setError("⚠️ " + result.message);
    }
  };

  return (
    <div className="login-page">
      <div className="login-container animate">
        <h2>Login to Court Summarizer</h2>
        <form onSubmit={handleSubmit}>
          {error && <p className="error-msg">{error}</p>}
          {success && <p className="success-msg">{success}</p>}

          <label htmlFor="email">Email</label>
          <input
            type="email"
            id="email"
            placeholder="Enter your email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />

          <label htmlFor="password">Password</label>
          <input
            type="password"
            id="password"
            placeholder="Enter your password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />

          <button type="submit">Login</button>

          <p className="signup-text">
            Don't have an account?{" "}
            <a href="/Signup" className="signup-link">
              Sign Up
            </a>
          </p>
        </form>
      </div>
    </div>
  );
};

export default Login;
