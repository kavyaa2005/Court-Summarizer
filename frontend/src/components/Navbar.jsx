import React, { useState } from "react";
import { Link } from "react-router-dom"; // ✅ Import Link
import "../assets/styles/Navbar.css";
import logo from "../assets/images/Brown and Beige Retro Illustrative Law Firm Logo1.png";
import { useAuth } from "../context/AuthContext";

function Navbar() {
  const [isActive, setIsActive] = useState(false);
  const [showProfileMenu, setShowProfileMenu] = useState(false);
  const { user, logout } = useAuth();

  const toggleNavbar = () => {
    setIsActive(!isActive);
  };

  const handleLogout = () => {
    logout();
    window.location.href = '/login';
  };

  return (
    <nav className="navbar">
      <div className="logo">
        <img src={logo} alt="Court Summarizer Logo" />
      </div>

      {/* Toggle button for mobile */}
      <button className="toggle-btn" onClick={toggleNavbar}>
        ☰
      </button>

      {/* Navbar links */}
      <ul className={`navbar-links ${isActive ? "active" : ""}`}>
        <li><Link to="/">Home</Link></li>
        
        {user && <li><Link to="/case-record">Case Record</Link></li>}
        {!user && <li><Link to="/login">Sign-In</Link></li>}
        
        {user && (
          <li className="profile-dropdown">
            <button 
              className="profile-btn" 
              onClick={() => setShowProfileMenu(!showProfileMenu)}
            >
              👤 {user.name || 'Account'}
            </button>
            {showProfileMenu && (
              <div className="dropdown-menu">
                <Link to="/profile" className="dropdown-item">
                  📋 My Profile
                </Link>
                <button onClick={handleLogout} className="dropdown-item logout-item">
                  🚪 Logout
                </button>
              </div>
            )}
          </li>
        )}
      </ul>
    </nav>
  );
}

export default Navbar;
