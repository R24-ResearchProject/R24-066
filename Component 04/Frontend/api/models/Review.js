const mongoose = require('mongoose');

// Schema for Reviews
const reviewSchema = new mongoose.Schema({
  reviewDate: {
    type: Date,
    default: Date.now 
  },
  total: {
    type: Number,
    required: true
  },
  points: {
    type: Number,
    required: true
  },
  user: {
    type: String,
    required: true
  },
  activity: {
    type: String,
    required: true
  },
  subject: {
    type: String,
    required: true
  }
});

const Review = mongoose.model('Review', reviewSchema);

module.exports = Review;
