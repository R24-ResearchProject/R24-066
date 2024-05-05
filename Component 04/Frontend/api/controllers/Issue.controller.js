const IssueService = require('../services/Issues.service');

class IssueController {
  constructor() {
    this.issueService = new IssueService();
  }

  async getAllIssues(req, res) {
    try {
      const issues = await this.issueService.getAllIssues();
      res.json(issues);
    } catch (error) {
      res.status(500).json({ error: error.message });
    }
  }

  async createIssue(req, res) {
    try {
      const newissue = await this.issueService.createIssue(req.body);
      res.status(201).json(newissue);
    } catch (error) {
      res.status(400).json({ error: error.message });
    }
  }

  async getIssueById(req, res) {
    try {
      const issue = await this.issueService.getIssueById(req.params.id);
      res.json(issue);
    } catch (error) {
      res.status(404).json({ error: 'Garbage Point not found' });
    }
  }

  async deleteIssueById(req, res) {
    try {
      await this.issueService.deleteIssueById(req.params.id);
      res.sendStatus(204);
    } catch (error) {
      res.status(404).json({ error: 'Garbage Point not found' });
    }
  }

  async updateIssueById(req, res) {
    try {
      const updatedIssue = await this.issueService.updateIssueById(req.params.id, req.body);
      res.json(updatedIssue);
    } catch (error) {
      res.status(404).json({ error: 'Garbage Point not found' });
    }
  }
}

module.exports = IssueController;
