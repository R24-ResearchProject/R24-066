const express = require('express');
const NotificationController = require('../controllers/Notifications.controller');

const router = express.Router();
const notificationController = new NotificationController();

router.get('/', notificationController.getAllNotifications.bind(notificationController));
router.post('/', notificationController.createNotification.bind(notificationController));
router.get('/:id', notificationController.getNotificationById.bind(notificationController));
router.delete('/:id', notificationController.deleteNotificationById.bind(notificationController));
router.put('/:id', notificationController.updateNotificationById.bind(notificationController));

// Additional route for getting notifications by district ordered by date
router.get('/district/:district', notificationController.getNotificationsByDistrictOrderedByDate.bind(notificationController));

module.exports = router;
