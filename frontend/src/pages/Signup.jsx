import React, { useState } from "react";
import { useNavigate } from "react-router-dom"; // ✅ for redirection
import "../assets/styles/Signup.css"; 
import { useAuth } from "../context/AuthContext";
import {
  validateName,
  validateEmail,
  validatePassword,
  validateOccupation,
} from "../assets/scripts/Signup.js";

const Signup = () => {
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [occupation, setOccupation] = useState("");
  const [error, setError] = useState("");

  const navigate = useNavigate(); // ✅ hook for redirect
  const { login } = useAuth();

  const handleSignup = async (e) => {
    e.preventDefault();

    setError("");

    if (!validateName(name)) {
      setError("⚠️ Full name must be at least 3 characters and contain only letters.");
      return;
    }
    if (!validateEmail(email)) {
      setError("⚠️ Please provide a valid email address (e.g., example@mail.com).");
      return;
    }
    if (!validatePassword(password)) {
      setError(
        "⚠️ Password must be at least 6 characters, include uppercase, lowercase, a number, and a special character."
      );
      return;
    }
    if (!validateOccupation(occupation)) {
      setError("⚠️ Please choose your occupation from the list.");
      return;
    }

    try {
      const NODE_API_URL = import.meta.env.VITE_NODE_API_URL || 'http://localhost:5002/api/summaries';
      const apiBase = NODE_API_URL.replace('/api/summaries', '/api');
      const response = await fetch(`${apiBase}/signup`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          name,
          email,
          password,
          occupation,
        }),
      });

      const data = await response.json();

      if (response.ok) {
        alert("✅ Account created successfully! Redirecting to Home...");
        console.log("Signup successful:", data);
        // Auto-login user after signup
        login({ email, name, occupation });
        // Redirect to home after 1s
        setTimeout(() => {
          navigate("/");
        }, 1000);
      } else {
        setError(data.message || "Signup failed. Please try again.");
      }
    } catch (error) {
      console.error("Signup error:", error);
      setError("");
    }
  };

  return (
    <div className="signup-page">
      <div className="signup-container animate">
        <h2>Create Your Account</h2>
        <form onSubmit={handleSignup}>
          {error && <p className="error-msg">{error}</p>}

          <label htmlFor="name">Full Name</label>
          <input
            type="text"
            id="name"
            placeholder="Enter your full name"
            value={name}
            onChange={(e) => setName(e.target.value)}
            required
          />

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
            placeholder="Enter a strong password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
          <small className="password-hint">
            Must be 6+ chars, include uppercase, lowercase, number & special character.
          </small>

          <label htmlFor="occupation">Occupation</label>
          <select
            id="occupation"
            value={occupation}
            onChange={(e) => setOccupation(e.target.value)}
            required
          >
            <option value="">Select your occupation</option>
            <option value="Student">Student</option>
            <option value="Lawyer">Lawyer</option>
            <option value="Judge">Judge</option>
            <option value="Paralegal">Paralegal</option>
            <option value="Other">Other</option>
          </select>

          <button type="submit">Sign Up</button>

          <p className="login-text">
            Already have an account? <a href="/login">Sign-In</a>
          </p>
        </form>
      </div>
    </div>
  );
};

export default Signup;
