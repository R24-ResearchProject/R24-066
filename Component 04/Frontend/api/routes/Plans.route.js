const express = require('express');
const { PlanController, ActivityController } = require('../controllers/Plans.controller');
const router = express.Router();
const planController = new PlanController();
const activityController = new ActivityController();

// Plan routes
router.post('/', planController.createPlan.bind(planController));
router.get('/', planController.getAllPlans.bind(planController));
router.get('/:id', planController.getPlanById.bind(planController));
router.delete('/:id', planController.deletePlanById.bind(planController));
router.patch('/:id', planController.updatePlanById.bind(planController));
router.get('/user/:user', planController.getPlansByUser.bind(planController)); 


// Activity routes
router.post('/activities', activityController.createActivity.bind(activityController));
router.get('/activities', activityController.getAllActivities.bind(activityController));
router.get('/activities/:id', activityController.getActivityById.bind(activityController));
router.delete('/activities/:id', activityController.deleteActivityById.bind(activityController));
router.put('/activities/:id', activityController.updateActivityById.bind(activityController));

module.exports = router;
