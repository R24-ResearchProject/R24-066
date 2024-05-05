const express = require('express');
const PersonalInfoController = require('../controllers/PersonalInfo.controller');
const { body } = require('express-validator');
const router = express.Router();
const personalInfoController = new PersonalInfoController();

router.post('/', personalInfoController.createPersonalInfo.bind(personalInfoController));
router.get('/', personalInfoController.getAllPersonalInfo.bind(personalInfoController));
router.get('/:id', personalInfoController.getPersonalInfoById.bind(personalInfoController));
router.delete('/:id', personalInfoController.deletePersonalInfoById.bind(personalInfoController));
router.put('/:id', personalInfoController.updatePersonalInfoById.bind(personalInfoController));
router.get('/latest/:username', personalInfoController.getLatestPersonalInfoByUsername.bind(personalInfoController));

module.exports = router;
