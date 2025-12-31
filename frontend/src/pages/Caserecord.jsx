// src/pages/CaseRecord.jsx
import React, { useState, useEffect } from "react";
import { useAuth } from "../context/AuthContext";
import "../assets/styles/Caserecord.css";
import Swal from 'sweetalert2';

const NODE_API_BASE = import.meta.env.VITE_NODE_API_URL?.replace('/api/summaries', '') || 'http://localhost:5002';

const CaseRecord = () => {
  const { user } = useAuth();
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [currentPage, setCurrentPage] = useState(1);
  const itemsPerPage = 5;

  // Fetch user summaries on component mount
  useEffect(() => {
    if (user?.email) {
      fetchUserSummaries();
    } else {
      setLoading(false);
    }
  }, [user]);

  const fetchUserSummaries = async () => {
    try {
      const userEmail = user.email;
      
      if (!userEmail) {
        Swal.fire({
          icon: 'warning',
          title: 'Not Logged In',
          text: 'Please log in to view your summaries.',
        });
        setLoading(false);
        return;
      }

      const response = await fetch(`${NODE_API_BASE}/api/summaries/user/${userEmail}`);
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      const result = await response.json();

      if (result.summaries) {
        setData(result.summaries);
      } else {
        setData([]);
      }
    } catch (error) {
      console.error('Error fetching summaries:', error);
      Swal.fire({
        icon: 'error',
        title: 'Connection Error',
        text: 'Could not connect to the server. Make sure MongoDB and Node API are running.',
      });
      setData([]);
    } finally {
      setLoading(false);
    }
  };

  const handleDownload = async (summaryId, summaryFileName) => {
    try {
      // Fetch the full summary data
      const response = await fetch(`${NODE_API_BASE}/api/summaries/${summaryId}`);
      const result = await response.json();

      if (response.ok && result.summary) {
        // Create a downloadable JSON blob
        const blob = new Blob([JSON.stringify(result.summary.summaryData, null, 2)], {
          type: 'application/json'
        });
        const url = window.URL.createObjectURL(blob);
        const link = document.createElement('a');
        link.href = url;
        link.download = summaryFileName || `summary_${summaryId}.json`;
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        window.URL.revokeObjectURL(url);

        Swal.fire({
          icon: 'success',
          title: 'Downloaded!',
          text: 'Summary downloaded successfully.',
          timer: 2000,
          showConfirmButton: false
        });
      } else {
        throw new Error(result.message || 'Download failed');
      }
    } catch (error) {
      console.error('Download error:', error);
      Swal.fire({
        icon: 'error',
        title: 'Download Failed',
        text: 'Could not download the summary.',
      });
    }
  };

  const handleDelete = async (summaryId) => {
    const result = await Swal.fire({
      title: 'Are you sure?',
      text: "You won't be able to revert this!",
      icon: 'warning',
      showCancelButton: true,
      confirmButtonColor: '#d33',
      cancelButtonColor: '#3085d6',
      confirmButtonText: 'Yes, delete it!'
    });

    if (result.isConfirmed) {
      try {
        const response = await fetch(`${NODE_API_BASE}/api/summaries/${summaryId}`, {
          method: 'DELETE'
        });

        if (response.ok) {
          // Remove from local state
          setData(prevData => prevData.filter(item => item._id !== summaryId));
          
          Swal.fire({
            icon: 'success',
            title: 'Deleted!',
            text: 'Summary has been deleted.',
            timer: 2000,
            showConfirmButton: false
          });
        } else {
          throw new Error('Delete failed');
        }
      } catch (error) {
        console.error('Delete error:', error);
        Swal.fire({
          icon: 'error',
          title: 'Error',
          text: 'Could not delete the summary.',
        });
      }
    }
  };

  // Pagination logic
  const lastIndex = currentPage * itemsPerPage;
  const firstIndex = lastIndex - itemsPerPage;
  const currentItems = data.slice(firstIndex, lastIndex);
  const totalPages = Math.ceil(data.length / itemsPerPage);

  const handlePrev = () => {
    if (currentPage > 1) setCurrentPage(currentPage - 1);
  };

  const handleNext = () => {
    if (currentPage < totalPages) setCurrentPage(currentPage + 1);
  };

  if (loading) {
    return (
      <div className="history-page">
        <h2>📚 My Summaries</h2>
        <div className="loading">Loading your summaries...</div>
      </div>
    );
  }

  if (!user) {
    return (
      <div className="history-page">
        <h2>📚 My Summaries</h2>
        <div className="no-data">
          <p>Please log in to view your case summaries.</p>
        </div>
      </div>
    );
  }

  return (
    <div className="history-page">
      <h2 className="page-top-title">📚 My Summaries</h2>
      <div className="center-block">

        {data.length === 0 && (
          <div className="no-data">
            <p>No summaries found. Start by uploading a legal document!</p>
            <p className="helper-text">Go to Home → Upload PDF → View summaries here</p>
          </div>
        )}
      </div>

      {data.length !== 0 && (
        <>
          <div className="summary-stats">
            <div className="stat-card">
              <span className="stat-label">Total Cases</span>
              <span className="stat-value">{data.length}</span>
            </div>
            <div className="stat-card">
              <span className="stat-label">Current Page</span>
              <span className="stat-value">{currentPage} of {totalPages}</span>
            </div>
          </div>
          
          <div className="table-container">
            <table className="history-table">
              <thead>
                <tr>
                  <th>#</th>
                  <th>Username</th>
                  <th>Case Name</th>
                  <th>Summary File</th>
                  <th>Date Created</th>
                  <th>Actions</th>
                </tr>
              </thead>
              <tbody>
                {currentItems.map((item, index) => (
                  <tr key={item._id}>
                    <td>{firstIndex + index + 1}</td>
                    <td>{item.userEmail?.split('@')[0] || 'Unknown'}</td>
                    <td className="case-name">{item.caseName || item.originalFileName || 'Untitled'}</td>
                    <td>{item.summaryFileName || 'summary.json'}</td>
                    <td>{new Date(item.createdAt).toLocaleDateString('en-US', { 
                      year: 'numeric', 
                      month: 'short', 
                      day: 'numeric' 
                    })}</td>
                    <td>
                      <button 
                        className="download-btn"
                        onClick={() => handleDownload(item._id, item.summaryFileName)}
                        title="Download summary"
                      >
                        📥 Summary
                      </button>
                      {/* PDF option removed per request */}
                      <button 
                        className="delete-btn"
                        onClick={() => handleDelete(item._id)}
                        title="Delete summary"
                        style={{ marginLeft: 8 }}
                      >
                        🗑️ Delete
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>

            {/* Pagination */}
            {totalPages > 1 && (
              <div className="pagination">
                <button onClick={handlePrev} disabled={currentPage === 1}>
                  ← Prev
                </button>
                <span className="page-info">
                  Page {currentPage} of {totalPages}
                </span>
                <button onClick={handleNext} disabled={currentPage === totalPages}>
                  Next →
                </button>
              </div>
            )}
          </div>
        </>
      )}
    </div>
  );
};

export default CaseRecord;
