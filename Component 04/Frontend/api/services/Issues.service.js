const Issue = require('../models/Issue');

class IssueService {
  async getAllIssues() {
    return await Issue.find();
  }

  async createIssue(issueData) {
    return await Issue.create(issueData);
  }

  async getIssueById(id) {
    return await Issue.findById(id);
  }

  async deleteIssueById(id) {
    return await Issue.findByIdAndDelete(id);
  }

  async updateIssueById(id, updateData) {
    return await Issue.findByIdAndUpdate(id, updateData, { new: true });
  }
}

module.exports = IssueService;
