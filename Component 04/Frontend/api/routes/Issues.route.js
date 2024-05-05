const express = require('express');
const IssueController = require('../controllers/Issue.controller');
const { body } = require('express-validator');
const router = express.Router();
const issueController = new IssueController();

router.post('/', issueController.createIssue.bind(issueController));
router.get('/', issueController.getAllIssues.bind(issueController));
router.get('/:id', issueController.getIssueById.bind(issueController));
router.delete('/:id', issueController.deleteIssueById.bind(issueController));
router.put('/:id', issueController.updateIssueById.bind(issueController));

module.exports = router;
