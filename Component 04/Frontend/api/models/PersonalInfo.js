const mongoose = require('mongoose');

// Schema for Garbage Points
const personalInfoSchema = new mongoose.Schema({
  username: {
    type: String,
    required: true
  },
  age: {
    type: Number,
    default: 10
  },
  gender: {
    type: String,
    default: "Male"
  },
  studyHours: {
    type: Number,
    default: 0
  },
  sleepHours: {
    type: Number,
    default: 0
  },
  subjects: {
    type: [String], 
    default: []
  },
  favorite: {
    type: [String], 
    default: []
  },
});

const PersonalInfo = mongoose.model('PersonalInfo', personalInfoSchema);

module.exports = PersonalInfo;
