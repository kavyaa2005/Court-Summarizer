const express = require('express');
const Summary = require('../models/Summary');
const path = require('path');
const multer = require('multer');

const router = express.Router();

// Multer storage for uploaded PDFs
const uploadsPath = path.join(__dirname, '..', 'uploads');
const storage = multer.diskStorage({
  destination: function (req, file, cb) {
    cb(null, uploadsPath);
  },
  filename: function (req, file, cb) {
    const unique = Date.now() + '-' + Math.round(Math.random() * 1e9);
    const safeName = file.originalname.replace(/[^a-zA-Z0-9.\-_]/g, '_');
    cb(null, `${unique}-${safeName}`);
  }
});
const upload = multer({ storage });

// Save a new summary
router.post('/save', async (req, res) => {
  // Log incoming request for debugging
  console.log('POST /api/summaries/save - body:', JSON.stringify(req.body).slice(0, 1000));
  const { 
    userEmail, 
    caseName, 
    originalFileName, 
    summaryFileName, 
    summaryData,
    summaryPath 
  } = req.body;

  if (!userEmail || !caseName || !summaryFileName) {
    return res.status(400).json({ message: 'Required fields missing.' });
  }

  try {
    const newSummary = new Summary({
      userEmail,
      caseName,
      originalFileName: originalFileName || caseName,
      summaryFileName,
      summaryData: summaryData || {},
      summaryPath: summaryPath || ''
    });

    await newSummary.save();

    res.status(201).json({ 
      message: 'Summary saved successfully.',
      summary: newSummary 
    });
  } catch (error) {
    console.error('Save summary error:', error);
    res.status(500).json({ message: 'Server error while saving summary.' });
  }
});

// Save a new summary and store uploaded PDF file (multipart/form-data)
router.post('/save-with-file', upload.single('file'), async (req, res) => {
  try {
    // fields come in req.body; summaryData may be a JSON string
    const {
      userEmail,
      caseName,
      originalFileName,
      summaryFileName,
      summaryData
    } = req.body;

    if (!userEmail || !caseName || !summaryFileName) {
      return res.status(400).json({ message: 'Required fields missing.' });
    }

    let parsedSummary = {};
    try {
      parsedSummary = typeof summaryData === 'string' ? JSON.parse(summaryData) : summaryData || {};
    } catch (e) {
      parsedSummary = { raw: summaryData };
    }

    const filePath = req.file ? `/uploads/${req.file.filename}` : '';

    const newSummary = new Summary({
      userEmail,
      caseName,
      originalFileName: originalFileName || caseName,
      summaryFileName,
      summaryData: parsedSummary,
      summaryPath: filePath
    });

    await newSummary.save();

    res.status(201).json({ message: 'Summary and file saved successfully.', summary: newSummary });
  } catch (error) {
    console.error('Save-with-file error:', error);
    res.status(500).json({ message: 'Server error while saving summary with file.' });
  }
});

// Get all summaries for a user
router.get('/user/:email', async (req, res) => {
  const { email } = req.params;

  try {
    const summaries = await Summary.find({ userEmail: email })
      .sort({ createdAt: -1 }); // Most recent first

    res.status(200).json({ 
      summaries,
      count: summaries.length 
    });
  } catch (error) {
    console.error('Fetch summaries error:', error);
    res.status(500).json({ message: 'Server error while fetching summaries.' });
  }
});

// Get a specific summary by ID
router.get('/:id', async (req, res) => {
  const { id } = req.params;

  try {
    const summary = await Summary.findById(id);
    
    if (!summary) {
      return res.status(404).json({ message: 'Summary not found.' });
    }

    res.status(200).json({ summary });
  } catch (error) {
    console.error('Fetch summary error:', error);
    res.status(500).json({ message: 'Server error while fetching summary.' });
  }
});

// Delete a summary
router.delete('/:id', async (req, res) => {
  const { id } = req.params;

  try {
    const summary = await Summary.findByIdAndDelete(id);

    if (!summary) {
      return res.status(404).json({ message: 'Summary not found.' });
    }

    // If an uploaded PDF exists, remove it from disk
    try {
      if (summary.summaryPath) {
        const fs = require('fs');
        const uploadsRoot = path.join(__dirname, '..', 'uploads');
        // summaryPath is like /uploads/<filename>
        const filename = summary.summaryPath.split('/').pop();
        const fullPath = path.join(uploadsRoot, filename);
        if (fs.existsSync(fullPath)) {
          fs.unlinkSync(fullPath);
          console.log('Deleted uploaded file:', fullPath);
        }
      }
    } catch (e) {
      console.error('Error removing uploaded file:', e);
    }

    res.status(200).json({ message: 'Summary deleted successfully.' });
  } catch (error) {
    console.error('Delete summary error:', error);
    res.status(500).json({ message: 'Server error while deleting summary.' });
  }
});

module.exports = router;
