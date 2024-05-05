const NotificationService = require('../services/Notidications.service');

class NotificationController {
  constructor() {
    this.notificationService = new NotificationService();
  }

  async getAllNotifications(req, res) {
    try {
      const notifications = await this.notificationService.getAllNotifications();
      res.json(notifications);
    } catch (error) {
      res.status(500).json({ error: error.message });
    }
  }

  async createNotification(req, res) {
    try {
      const newNotification = await this.notificationService.createNotification(req.body);
      res.status(201).json(newNotification);
    } catch (error) {
      res.status(400).json({ error: error.message });
    }
  }

  async getNotificationById(req, res) {
    try {
      const notification = await this.notificationService.getNotificationById(req.params.id);
      res.json(notification);
    } catch (error) {
      res.status(404).json({ error: 'Notification not found' });
    }
  }

  async deleteNotificationById(req, res) {
    try {
      await this.notificationService.deleteNotificationById(req.params.id);
      res.sendStatus(204);
    } catch (error) {
      res.status(404).json({ error: 'Notification not found' });
    }
  }

  async updateNotificationById(req, res) {
    try {
      const updatedNotification = await this.notificationService.updateNotificationById(req.params.id, req.body);
      res.json(updatedNotification);
    } catch (error) {
      res.status(404).json({ error: 'Notification not found' });
    }
  }

  async getNotificationsByDistrictOrderedByDate(req, res) {
    try {
      const notifications = await this.notificationService.getNotificationsByDistrictOrderedByDate(req.params.district);
      res.json(notifications);
    } catch (error) {
      res.status(500).json({ error: error.message });
    }
  }
}

module.exports = NotificationController;
