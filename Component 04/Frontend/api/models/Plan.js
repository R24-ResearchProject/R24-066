const mongoose = require('mongoose');

// Schema for Activity
const activitySchema = new mongoose.Schema({
  type: {
    type: String,
    required: true
  },
  subject: {
    type: String,
    required: true
  },
  startTime: {
    type: Date,
    required: true
  },
  hours: {
    type: Number,
    required: true
  },
  planID: {
    type: mongoose.Schema.Types.ObjectId,
    ref: 'Plan',
    default: null
  }
});

const Activity = mongoose.model('Activity', activitySchema);

// Schema for Plan
const planSchema = new mongoose.Schema({
  title: {
    type: String,
    required: true
  },
  description: {
    type: String,
    default: ''
  },
  activities: [activitySchema],
  status: {
    type: String,
    default: 'PENDING'
  },
  user: {
    type: String,
  }
});

const Plan = mongoose.model('Plan', planSchema);

module.exports = { Plan, Activity };
