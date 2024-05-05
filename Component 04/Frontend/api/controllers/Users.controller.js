const userService = require("../services/Users.service");

class UserController {
  async createUser(req, res) {
    try {
      const savedUser = await userService.createUser(req.body);
      res.status(200).json(savedUser);
    } catch (err) {
      console.log(err);
      console.log(err.code);
      if (err.code === 11000 && err.keyPattern.email) {
        // Email duplication error
        return res.status(400).json({ error: 'Email already exists' });
      }
      res.status(500).json(err);
    }
  }

  async updateUser(req, res) {
    try {
      const updatedUser = await userService.updateUser(
        req.params.id,
        req.body
      );
      res.status(200).json(updatedUser);
    } catch (err) {
      res.status(500).json(err);
    }
  }

  async deleteUser(req, res) {
    try {
      await userService.deleteUser(req.params.id);
      res.status(200).json("User has been deleted.");
    } catch (err) {
      res.status(500).json(err);
    }
  }

  async getUserById(req, res) {
    try {
      const user = await userService.getUserById(req.params.id);
      res.status(200).json(user);
    } catch (err) {
      res.status(500).json(err);
    }
  }

  async getUserByUsername(req, res) {
    try {
      const user = await userService.getUserByUsername(req.params.id);
      res.status(200).json(user);
    } catch (err) {
      res.status(500).json(err);
    }
  }

  async getAllUsers(req, res) {
    try {
      const users = await userService.getAllUsers();
      res.status(200).json(users);
    } catch (err) {
      console.log(err);
      res.status(500).json(err);
    }
  }
}

module.exports = new UserController();
