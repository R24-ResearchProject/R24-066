const Notification = require('../models/Notification');

class NotificationService {
  async getAllNotifications() {
    return await Notification.find();
  }

  async createNotification(notificationData) {
    return await Notification.create(notificationData);
  }

  async getNotificationById(id) {
    return await Notification.findById(id);
  }

  async deleteNotificationById(id) {
    return await Notification.findByIdAndDelete(id);
  }

  async updateNotificationById(id, updateData) {
    return await Notification.findByIdAndUpdate(id, updateData, { new: true });
  }

  async getNotificationsByDistrictOrderedByDate(district) {
    return await Notification.find({ district }).sort({ createdAt: -1 });
  }
}

module.exports = NotificationService;
