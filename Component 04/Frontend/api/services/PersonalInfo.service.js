const PersonalInfo = require('../models/PersonalInfo');

class PersonalInfoService {
  async getAllPersonalInfo() {
    return await PersonalInfo.find();
  }

  async createPersonalInfo(personalInfoData) {
    return await PersonalInfo.create(personalInfoData);
  }

  async getPersonalInfoById(id) {
    return await PersonalInfo.findById(id);
  }

  async deletePersonalInfoById(id) {
    return await PersonalInfo.findByIdAndDelete(id);
  }

  async updatePersonalInfoById(id, updateData) {
    return await PersonalInfo.findByIdAndUpdate(id, updateData, { new: true });
  }

  async getLatestPersonalInfoByUsername(username) {
    return await PersonalInfo.findOne({ username }).sort({ createdAt: -1 }).limit(1);
  }
}

module.exports = PersonalInfoService;
