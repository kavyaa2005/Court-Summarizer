import React, { useState } from "react";
import { useAuth } from "../../context/AuthContext";
import "../../assets/styles/Upload.css";

// Prefer env-configured API URL, fallback to localhost:8000
const FASTAPI_URL = import.meta.env.VITE_FASTAPI_URL || "http://localhost:8000";
const NODE_API_BASE = import.meta.env.VITE_NODE_API_URL?.replace('/api/summaries', '') || 'http://localhost:5002';

const UploadModal = ({ isOpen, onClose }) => {
  const { user } = useAuth();
  const [file, setFile] = useState(null);
  const [uploading, setUploading] = useState(false);

  if (!isOpen) return null;

  const handleFileChange = (event) => {
    setFile(event.target.files[0]);
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    if (!file) {
      alert("Please select a PDF file first.");
      return;
    }

    if (!user?.email) {
      alert("Please log in to save your summaries.");
      return;
    }

    setUploading(true);
    const formData = new FormData();
    formData.append("file", file);

    try {
      // Quick health check for clearer feedback
      try {
        const health = await fetch(`${FASTAPI_URL}/health`);
        if (!health.ok) throw new Error("Health check failed");
      } catch (e) {
        alert("❌ FastAPI not reachable at " + FASTAPI_URL + ". Is the server running?");
        setUploading(false);
        return;
      }

      const response = await fetch(`${FASTAPI_URL}/summarize_pdf`, {
        method: "POST",
        body: formData,
      });

      if (!response.ok) throw new Error("API error");

      // 👇 Get the file blob (JSON)
      const blob = await response.blob();
      
      // 👇 Parse the JSON to save to database
      const summaryText = await blob.text();
      const summaryData = JSON.parse(summaryText);

      // 👇 Save to MongoDB via Node API, including the original PDF file
      try {
        const form = new FormData();
        form.append('file', file);
        form.append('userEmail', user.email);
        form.append('caseName', file.name.replace('.pdf', ''));
        form.append('originalFileName', file.name);
        form.append('summaryFileName', `${file.name}_summary.json`);
        form.append('summaryData', JSON.stringify(summaryData));

        const saveWithFileResponse = await fetch(`${NODE_API_BASE}/api/summaries/save-with-file`, {
          method: 'POST',
          body: form
        });

        let saveResult = null;
        try { saveResult = await saveWithFileResponse.json(); } catch (e) { /* ignore parse */ }

        if (!saveWithFileResponse.ok) {
          console.warn('Failed to save summary+file to database', saveWithFileResponse.status, saveResult);
          alert('⚠️ Summary processed but failed to save file to database. Check Node API / MongoDB.');
        } else {
          console.log('Saved summary+file response:', saveResult);
        }
      } catch (err) {
        console.error('Save-with-file error:', err);
        alert('⚠️ Failed to save summary and file to server.');
      }

      // 👇 Create download link
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = `${file.name}_summary.json`; // downloaded file name
      document.body.appendChild(a);
      a.click();
      a.remove();

      alert("✅ Summary downloaded and saved to your history!");
      setFile(null);
      setTimeout(() => onClose(), 1000);
    } catch (error) {
      console.error("Upload error:", error);
      alert("❌ Something went wrong. Check if FastAPI is running.");
    } finally {
      setUploading(false);
    }
  };

  return (
    <div className="modal-overlay">
      <div className="modal-container">
        <h2 className="modal-title">Upload Your PDF</h2>
        <form className="upload-form" onSubmit={handleSubmit}>
          <input
            type="file"
            accept="application/pdf"
            className="file-input"
            onChange={handleFileChange}
            disabled={uploading}
          />
          <button type="submit" className="upload-btn" disabled={uploading}>
            {uploading ? '⏳ Processing...' : '📤 Upload & Summarize'}
          </button>
        </form>
        
        {file && (
          <p className="file-selected">Selected: {file.name}</p>
        )}

        <button className="close-btn" onClick={onClose} disabled={uploading}>
          ✖ Close
        </button>
      </div>
    </div>
  );
};

export default UploadModal;
