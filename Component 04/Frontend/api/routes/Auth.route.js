const router = require("express").Router();
const User = require("../models/User");
const CryptoJS = require("crypto-js");
const jwt = require("jsonwebtoken");

//LOGIN

router.post("/sign-in", async (req, res) => {
  console.log(req.body);
  // let role = 'User';
  try {
    let user = await User.findOne({ username: req.body.username });

    // If not found, search in Doctor collection
    if (!user) {
      // role = 'Garbage Collector';
      // user = await GarbageCollector.findOne({ username: req.body.username });
    }

    if (!user) {
      return res.status(401).json("Wrong credentials! Try Again!");
    }

    console.log(user);

    const hashedPassword = CryptoJS.AES.decrypt(
      user.password,
      process.env.PASS_SEC
    );
    const originalPassword = hashedPassword.toString(CryptoJS.enc.Utf8);

    if (originalPassword !== req.body.password) {
      return res.status(401).json("Wrong credentials!");
    }

    const accessToken = jwt.sign(
      {
        id: user._id,
        role:user.role,
      },
      process.env.JWT_SEC,
      { expiresIn: "1d" }
    );

    const { password, ...others } = user._doc;

    if (!res.headersSent) {
      res.status(200).json({ ...others, accessToken });
    } else {
      console.log("Headers already sent. Cannot send response.");
    }
  } catch (err) {
    console.log(err);
    if (!res.headersSent) {
      res.status(500).json(err);
    } else {
      console.log("Headers already sent. Cannot send error response.");
    }
  }
});


module.exports = router;
