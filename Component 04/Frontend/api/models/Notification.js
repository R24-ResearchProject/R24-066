const mongoose = require('mongoose');

// Schema for Notification
const notificationSchema = new mongoose.Schema({
  title: {
    type: String,
    required: true
  },
  message: {
    type: String,
    required: true
  },
  district: {
    type: String,
    required: true
  },
  status: {
    type: String,
    default: "valid"
  },
  createdAt: {
    type: Date,
    default: Date.now
  }
});

const Notification = mongoose.model('Notification', notificationSchema);

module.exports = Notification;
