// API helper functions for summary operations
import Swal from 'sweetalert2';

// Use env-configured Node API base URL, fallback to localhost:5001
const API_BASE_URL = import.meta.env.VITE_NODE_API_URL || 'http://localhost:5001/api/summaries';

/**
 * Save a summary to the database after processing
 * @param {Object} summaryData - The summary data from FastAPI
 * @param {string} caseName - Name of the case
 * @param {string} fileName - Original file name
 * @returns {Promise<Object>} Response from the server
 */
export const saveSummaryToDatabase = async (summaryData, caseName, fileName) => {
  const userEmail = localStorage.getItem('userEmail');
  
  if (!userEmail) {
    console.error('User not logged in');
    Swal.fire({
      icon: 'warning',
      title: 'Not Logged In',
      text: 'Please log in to save summaries.',
    });
    return { success: false, message: 'User not logged in' };
  }

  try {
    const response = await fetch(`${API_BASE_URL}/save`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        userEmail,
        caseName: caseName || 'Unnamed Case',
        originalFileName: fileName,
        summaryFileName: `${fileName.replace('.pdf', '')}_summary.json`,
        summaryData: summaryData,
      }),
    });

    const result = await response.json();

    if (response.ok) {
      console.log('Summary saved successfully:', result);
      Swal.fire({
        icon: 'success',
        title: 'Saved!',
        text: 'Summary saved to your records.',
        timer: 2000,
        showConfirmButton: false
      });
      return { success: true, data: result };
    } else {
      console.error('Failed to save summary:', result.message);
      Swal.fire({
        icon: 'error',
        title: 'Save Failed',
        text: result.message || 'Could not save the summary.',
      });
      return { success: false, message: result.message };
    }
  } catch (error) {
    console.error('Error saving summary:', error);
    Swal.fire({
      icon: 'error',
      title: 'Connection Error',
      text: 'Could not connect to the server.',
    });
    return { success: false, message: error.message };
  }
};

/**
 * Fetch all summaries for the logged-in user
 * @returns {Promise<Array>} Array of summaries
 */
export const fetchUserSummaries = async () => {
  const userEmail = localStorage.getItem('userEmail');
  
  if (!userEmail) {
    return { success: false, message: 'User not logged in', summaries: [] };
  }

  try {
    const response = await fetch(`${API_BASE_URL}/user/${userEmail}`);
    const result = await response.json();

    if (response.ok) {
      return { success: true, summaries: result.summaries, count: result.count };
    } else {
      return { success: false, message: result.message, summaries: [] };
    }
  } catch (error) {
    console.error('Error fetching summaries:', error);
    return { success: false, message: error.message, summaries: [] };
  }
};

/**
 * Delete a summary by ID
 * @param {string} summaryId - The ID of the summary to delete
 * @returns {Promise<Object>} Response from the server
 */
export const deleteSummary = async (summaryId) => {
  try {
    const response = await fetch(`${API_BASE_URL}/${summaryId}`, {
      method: 'DELETE'
    });

    const result = await response.json();

    if (response.ok) {
      return { success: true, message: result.message };
    } else {
      return { success: false, message: result.message };
    }
  } catch (error) {
    console.error('Error deleting summary:', error);
    return { success: false, message: error.message };
  }
};

/**
 * Download a summary by ID
 * @param {string} summaryId - The ID of the summary to download
 * @param {string} fileName - Name for the downloaded file
 * @returns {Promise<Object>} Response from the server
 */
export const downloadSummary = async (summaryId, fileName) => {
  try {
    const response = await fetch(`${API_BASE_URL}/${summaryId}`);
    const result = await response.json();

    if (response.ok) {
      // Create a downloadable JSON blob
      const blob = new Blob([JSON.stringify(result.summary.summaryData, null, 2)], {
        type: 'application/json'
      });
      const url = window.URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      link.download = fileName;
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      window.URL.revokeObjectURL(url);

      return { success: true };
    } else {
      return { success: false, message: result.message };
    }
  } catch (error) {
    console.error('Error downloading summary:', error);
    return { success: false, message: error.message };
  }
};
