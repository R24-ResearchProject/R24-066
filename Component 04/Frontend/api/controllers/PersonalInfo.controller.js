const PersonalInfoService = require('../services/PersonalInfo.service');

class PersonalInfoController {
  constructor() {
    this.personalInfoService = new PersonalInfoService();
  }

  async getAllPersonalInfo(req, res) {
    try {
      const personalInfo = await this.personalInfoService.getAllPersonalInfo();
      res.json(personalInfo);
    } catch (error) {
      res.status(500).json({ error: error.message });
    }
  }

  async createPersonalInfo(req, res) {
    try {
      const newPersonalInfo = await this.personalInfoService.createPersonalInfo(req.body);
      res.status(201).json(newPersonalInfo);
    } catch (error) {
      res.status(400).json({ error: error.message });
    }
  }

  async getPersonalInfoById(req, res) {
    try {
      const personalInfo = await this.personalInfoService.getPersonalInfoById(req.params.id);
      res.json(personalInfo);
    } catch (error) {
      res.status(404).json({ error: 'Personal Info not found' });
    }
  }

  async deletePersonalInfoById(req, res) {
    try {
      await this.personalInfoService.deletePersonalInfoById(req.params.id);
      res.sendStatus(204);
    } catch (error) {
      res.status(404).json({ error: 'Personal Info not found' });
    }
  }

  async updatePersonalInfoById(req, res) {
    try {
      const updatedPersonalInfo = await this.personalInfoService.updatePersonalInfoById(req.params.id, req.body);
      res.json(updatedPersonalInfo);
    } catch (error) {
      res.status(404).json({ error: 'Personal Info not found' });
    }
  }

  async getLatestPersonalInfoByUsername(req, res) {
    try {
      const latestPersonalInfo = await this.personalInfoService.getLatestPersonalInfoByUsername(req.params.username);
      res.json(latestPersonalInfo);
    } catch (error) {
      res.status(404).json({ error: 'Personal Info not found' });
    }
  }
}

module.exports = PersonalInfoController;
