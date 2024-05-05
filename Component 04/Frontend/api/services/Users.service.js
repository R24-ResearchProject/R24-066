const User = require("../models/User");
const CryptoJS = require("crypto-js");

class UserService {
  async createUser(userData) {
    console.log("userData")
    console.log(userData)
    const newUser = new User(userData);
    try {
      newUser.password = CryptoJS.AES.encrypt(
          newUser.password,
          process.env.PASS_SEC
        ).toString();
      const savedUser = await newUser.save();
      return savedUser;
    } catch (err) {
      throw err;
    }
  }

  async updateUser(id, updatedData) {
    try {
      const updatedUser = await User.findByIdAndUpdate(
        id,
        {
          $set: updatedData,
        },
        { new: true }
      );
      return updatedUser;
    } catch (err) {
      throw err;
    }
  }

  async deleteUser(id) {
    try {
      await User.findByIdAndDelete(id);
    } catch (err) {
      throw err;
    }
  }

  async getUserById(id) {
    try {
      const user = await User.findById(id);
      return user;
    } catch (err) {
      throw err;
    }
  }

  async getUserByUsername(id) {
    try {
      const user = await User.find({username: id});
      return user;
    } catch (err) {
      throw err;
    }
  }

  async getAllUsers() {
    try {
        const user = await User.find();
        return user;
    } catch (err) {
      throw err;
    }
  }
  
}

module.exports = new UserService();
