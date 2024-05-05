const { PlanService, ActivityService } = require('../services/Plan.service');

class PlanController {
  constructor() {
    this.planService = new PlanService();
  }

  async getAllPlans(req, res) {
    try {
      const plans = await this.planService.getAllPlans();
      res.json(plans);
    } catch (error) {
      res.status(500).json({ error: error.message });
    }
  }

  async createPlan(req, res) {
    console.log(req.body)
    try {
      if (req.body._id) {
        const updatedPlan = await this.planService.updatePlanById(req.body._id, req.body);
        res.json(updatedPlan);
      } else {
        // Create new plan
        const newPlan = await this.planService.createPlan(req.body);
        res.status(201).json(newPlan);
      }
    } catch (error) {
      res.status(400).json({ error: error.message });
    }
  }

  async getPlanById(req, res) {
    try {
      const plan = await this.planService.getPlanById(req.params.id);
      res.json(plan);
    } catch (error) {
      res.status(404).json({ error: 'Plan not found' });
    }
  }

  async deletePlanById(req, res) {
    try {
      await this.planService.deletePlanById(req.params.id);
      res.sendStatus(204);
    } catch (error) {
      res.status(404).json({ error: 'Plan not found' });
    }
  }

  async updatePlanById(req, res) {
    try {
      const updatedPlan = await this.planService.updatePlanById(req.params.id, req.body);
      res.json(updatedPlan);
    } catch (error) {
      res.status(404).json({ error: 'Plan not found' });
    }
  }

  async getPlansByUser(req, res) {
    try {
      const { user } = req.params;
      const plans = await this.planService.getPlansByUser(user);
      res.json(plans);
    } catch (error) {
      res.status(500).json({ error: error.message });
    }
  }
}

class ActivityController {
  constructor() {
    this.activityService = new ActivityService();
  }

  async getAllActivities(req, res) {
    try {
      const activities = await this.activityService.getAllActivities();
      res.json(activities);
    } catch (error) {
      res.status(500).json({ error: error.message });
    }
  }

  async createActivity(req, res) {
    console.log(req.body)
    try {
      const newActivity = await this.activityService.createActivity(req.body);
      res.status(201).json(newActivity);
    } catch (error) {
      res.status(400).json({ error: error.message });
    }
  }

  async getActivityById(req, res) {
    try {
      const activity = await this.activityService.getActivityById(req.params.id);
      res.json(activity);
    } catch (error) {
      res.status(404).json({ error: 'Activity not found' });
    }
  }

  async deleteActivityById(req, res) {
    try {
      await this.activityService.deleteActivityById(req.params.id);
      res.sendStatus(204);
    } catch (error) {
      res.status(404).json({ error: 'Activity not found' });
    }
  }

  async updateActivityById(req, res) {
    try {
      const updatedActivity = await this.activityService.updateActivityById(req.params.id, req.body);
      res.json(updatedActivity);
    } catch (error) {
      res.status(404).json({ error: 'Activity not found' });
    }
  }
}

module.exports = { PlanController, ActivityController };
