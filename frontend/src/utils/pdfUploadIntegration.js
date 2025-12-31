/**
 * INTEGRATION GUIDE: How to integrate Summary Saving with PDF Upload
 * 
 * Add this code to your PDF upload component where you process the document
 * with FastAPI and get the summary response.
 */

import { saveSummaryToDatabase } from '../utils/summaryApi';

/**
 * Example: After uploading PDF to FastAPI and getting summary response
 * 
 * Typical flow:
 * 1. User uploads PDF file
 * 2. Send PDF to FastAPI (http://localhost:8000/summarize)
 * 3. FastAPI processes and returns summary
 * 4. Save summary to MongoDB using this function
 */

export const handlePdfUploadAndSave = async (file) => {
  try {
    // Step 1: Create FormData with the PDF file
    const formData = new FormData();
    formData.append('file', file);

    // Step 2: Send to FastAPI for processing
    const response = await fetch('http://localhost:8000/summarize', {
      method: 'POST',
      body: formData,
    });

    if (!response.ok) {
      throw new Error('Failed to process document');
    }

    const summaryData = await response.json();

    // Step 3: Extract case name from summary or use filename
    const caseName = summaryData.case_name || 
                    summaryData.title || 
                    file.name.replace('.pdf', '');

    // Step 4: Save to MongoDB database
    const saveResult = await saveSummaryToDatabase(
      summaryData,           // Full summary data from FastAPI
      caseName,              // Case name
      file.name              // Original filename
    );

    if (saveResult.success) {
      console.log('✅ Summary saved to database:', saveResult.data);
      return {
        success: true,
        summary: summaryData,
        saved: saveResult.data
      };
    } else {
      console.error('❌ Failed to save summary:', saveResult.message);
      return {
        success: true,  // Processing was successful
        summary: summaryData,
        saved: false,
        error: saveResult.message
      };
    }

  } catch (error) {
    console.error('Error processing PDF:', error);
    return {
      success: false,
      error: error.message
    };
  }
};

/**
 * USAGE IN YOUR COMPONENT:
 * 
 * import { handlePdfUploadAndSave } from './path/to/this/file';
 * 
 * const YourUploadComponent = () => {
 *   const handleFileSelect = async (event) => {
 *     const file = event.target.files[0];
 *     
 *     if (file && file.type === 'application/pdf') {
 *       const result = await handlePdfUploadAndSave(file);
 *       
 *       if (result.success) {
 *         // Show summary to user
 *         console.log('Summary:', result.summary);
 *         
 *         if (result.saved) {
 *           console.log('Also saved to database!');
 *         }
 *       } else {
 *         console.error('Processing failed:', result.error);
 *       }
 *     }
 *   };
 * 
 *   return (
 *     <input 
 *       type="file" 
 *       accept=".pdf" 
 *       onChange={handleFileSelect}
 *     />
 *   );
 * };
 */
