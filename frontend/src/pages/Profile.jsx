import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import '../assets/styles/Profile.css';

const Profile = () => {
  const { user, logout } = useAuth();
  const navigate = useNavigate();
  const [showModal, setShowModal] = useState(true);

  const displayName = (user && user.name && user.name.trim())
    ? user.name
    : (user && user.email ? user.email.split('@')[0] : 'User Account');

  const displayOccupation = (user && user.occupation && user.occupation.trim())
    ? user.occupation
    : 'Not specified';

  // If user object is missing name/occupation, try to fetch fresh record from backend
  const { updateUser } = useAuth();
  React.useEffect(() => {
    const tryRefresh = async () => {
      if (!user) return;
      const needsName = !(user.name && user.name.trim());
      const needsOcc = !(user.occupation && user.occupation.trim());
      if (!needsName && !needsOcc) return;

      const storedEmail = localStorage.getItem('userEmail') || user.email;
      if (!storedEmail) return;

      try {
        const NODE_API_URL = import.meta.env.VITE_NODE_API_URL || 'http://localhost:5002/api/summaries';
        const apiBase = NODE_API_URL.replace('/api/summaries', '/api');
        const res = await fetch(`${apiBase}/user?email=${encodeURIComponent(storedEmail)}`);
        if (res.ok) {
          const data = await res.json();
          const updated = {
            name: data.name || user.name || '',
            occupation: data.occupation || user.occupation || '',
            email: data.email || user.email,
          };
          updateUser(updated);
        }
      } catch (e) {
        console.warn('Failed to refresh user profile:', e);
      }
    };
    tryRefresh();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [user]);

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  const handleClose = () => {
    setShowModal(false);
    setTimeout(() => navigate('/'), 300);
  };

  if (!showModal) return null;

  return (
    <div className="profile-modal-overlay" onClick={handleClose}>
      <div className="profile-modal-container" onClick={(e) => e.stopPropagation()}>
        {/* Close Button */}
        <button className="modal-close-btn" onClick={handleClose}>
          ✕
        </button>

        {/* Header with gradient */}
        <div className="profile-modal-header">
          <div className="profile-avatar-large">
            {(user && (user.name || user.email))
              ? (user.name ? user.name.charAt(0).toUpperCase() : user.email.charAt(0).toUpperCase())
              : 'U'}
          </div>
          <h2>{displayName}</h2>
          <p className="profile-email">{user?.email || 'No email'}</p>
        </div>

        {/* Details Section */}
        <div className="profile-modal-body">
          <div className="profile-info-row">
            <span className="info-label">👤 Full Name</span>
            <span className="info-value">{displayName}</span>
          </div>

          <div className="profile-info-row">
            <span className="info-label">📧 Email Address</span>
            <span className="info-value">{user?.email || 'N/A'}</span>
          </div>

          <div className="profile-info-row">
            <span className="info-label">💼 Occupation</span>
            <span className="info-value">{displayOccupation}</span>
          </div>
        </div>

        {/* Action Buttons */}
        <div className="profile-modal-footer">
          <button className="modal-action-btn primary-gradient" onClick={() => navigate('/case-record')}>
            📋 My Summaries
          </button>
          <button className="modal-action-btn secondary-outline" onClick={handleClose}>
            🏠 Back to Home
          </button>
          <button className="modal-action-btn danger-btn" onClick={handleLogout}>
            🚪 Logout
          </button>
        </div>
      </div>
    </div>
  );
};

export default Profile;
