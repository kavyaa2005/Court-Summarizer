const mongoose = require('mongoose');

const SummarySchema = new mongoose.Schema({
  userId: {
    type: mongoose.Schema.Types.ObjectId,
    ref: 'User',
  },
  userEmail: {
    type: String,
    required: true
  },
  caseName: {
    type: String,
    required: true
  },
  originalFileName: {
    type: String,
    required: true
  },
  summaryFileName: {
    type: String,
    required: true
  },
  summaryData: {
    judges: [String],
    citations: [String],
    acts: [String],
    sections: [String],
    // Allow `summary` to be a string or an object (some summaries return structured objects)
    summary: mongoose.Schema.Types.Mixed,
    fullSummary: mongoose.Schema.Types.Mixed
  },
  summaryPath: {
    type: String
  }
}, {
  timestamps: true
});

module.exports = mongoose.model('Summary', SummarySchema);
