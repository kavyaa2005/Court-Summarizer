const express = require('express');
const mongoose = require('mongoose');
const cors = require('cors');
const dotenv = require('dotenv');
const authRoutes = require('./routes/auth');
const summaryRoutes = require('./routes/summaries');

dotenv.config();

const app = express();

// Use a different port if 5000 is in use
const PORT = process.env.PORT || 5001; // changed from 5000 to 5001

// Middleware
app.use(cors());
app.use(express.json());

// Request logging for debugging (will log method and url and short body)
app.use((req, res, next) => {
  try {
    const shortBody = req.body && Object.keys(req.body).length ? JSON.stringify(req.body).slice(0, 1000) : null;
    console.log(`[REQ] ${req.method} ${req.originalUrl} body:${shortBody}`);
  } catch (e) {
    console.log('[REQ] logging error', e);
  }
  next();
});

// Serve uploaded files statically from /uploads
const path = require('path');
const fs = require('fs');
const uploadsDir = path.join(__dirname, 'uploads');
if (!fs.existsSync(uploadsDir)) {
  fs.mkdirSync(uploadsDir, { recursive: true });
}
app.use('/uploads', express.static(uploadsDir));

// Routes
app.use('/api', authRoutes);
app.use('/api/summaries', summaryRoutes);

// MongoDB connection
const mongoUri = process.env.MONGODB_URI || 'mongodb://localhost:27017/court-summarizer';

mongoose.connect(mongoUri, {
  useNewUrlParser: true,
  useUnifiedTopology: true,
})
.then(() => {
  console.log('Connected to MongoDB');
  
  // Start the server
  const server = app.listen(PORT, () => {
    console.log(`Server running on port ${PORT}`);
  });

  // Handle "port already in use" error gracefully
  server.on('error', (err) => {
    if (err.code === 'EADDRINUSE') {
      console.error(`Port ${PORT} is already in use. Try changing the PORT number.`);
    } else {
      console.error(err);
    }
  });

})
.catch((err) => {
  console.error('Failed to connect to MongoDB', err);
  console.log('Please ensure MongoDB is installed and running locally.');
});
