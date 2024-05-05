const mongoose = require('mongoose');

// Schema for Garbage Points
const issueSchema = new mongoose.Schema({
  title: {
    type: String,
    required: true
  },
  description: {
    type: String,
    default: ''
  },
  location: {
    type: Object, 
    required: true,
    default: {}
  },
  status: {
    type: String,
    default: "PENDING",
    
  },
  image: {
    type: String,
    default: ''
  }
});

const Issue = mongoose.model('Issue', issueSchema);

module.exports = Issue;
