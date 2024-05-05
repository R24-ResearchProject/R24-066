const express = require("express");
const router = express.Router();
const { body } = require('express-validator');
const userController = require("../controllers/Users.controller");

router.post("/", [
    // Validate fields
    body('username').notEmpty(),
    body('fullName').notEmpty(),
    body('nic').notEmpty(),
    body('email').isEmail(),
    body('password').notEmpty(),
    body('password').isLength({ min: 6 }),
  ], userController.createUser);
router.patch("/:id", [
    body('username').notEmpty(),
    body('fullName').notEmpty(),
    body('nic').notEmpty(),
    body('email').isEmail(),
], userController.updateUser);
router.delete("/:id", userController.deleteUser);
router.get("/:id", userController.getUserById);
router.get("/find/:id", userController.getUserByUsername);
router.get("/", userController.getAllUsers);

module.exports = router;
