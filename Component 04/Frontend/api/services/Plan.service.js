const {Plan, Activity} = require('../models/Plan');
// const Activity = require('../models/Activity');

class PlanService {
  async getAllPlans() {
    return await Plan.find();
  }

  async createPlan(planData) {
    return await Plan.create(planData);
  }

  async getPlanById(id) {
    return await Plan.findById(id);
  }

  async deletePlanById(id) {
    return await Plan.findByIdAndDelete(id);
  }

  async updatePlanById(id, updateData) {
    return await Plan.findByIdAndUpdate(id, updateData, { new: true });
  }

  async getPlansByUser(user) {
    return await Plan.find({ user });
  }
}

class ActivityService {
  async getAllActivities() {
    return await Activity.find();
  }

  async createActivity(activityData) {
    return await Activity.create(activityData);
  }

  async getActivityById(id) {
    return await Activity.findById(id);
  }

  async deleteActivityById(id) {
    return await Activity.findByIdAndDelete(id);
  }

  async updateActivityById(id, updateData) {
    return await Activity.findByIdAndUpdate(id, updateData, { new: true });
  }
}

module.exports = { PlanService, ActivityService };
