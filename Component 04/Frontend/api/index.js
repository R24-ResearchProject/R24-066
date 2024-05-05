const express = require('express');
const dotenv = require('dotenv');
const cors = require('cors');
const {readdirSync} = require('fs');
const { db } = require('./configs/configs');
dotenv.config()

const issuesRoute = require('./routes/Issues.route')
const userRoute = require('./routes/Users.route')
const authRoute = require('./routes/Auth.route')
const notificationRoute = require('./routes/Notifications.route')
const personalRoute = require('./routes/PersonalInfo.route')
const plansRoute = require('./routes/Plans.route')
const reviewsRoute = require('./routes/Reviews.route')

const app = express();
const port = process.env.PORT || 5001;

// CORS
app.use(express.json())
app.use(cors())



// Define routes
app.get('/', (req, res) => {
    res.send('App is Running!');
});

app.use("/api/users", userRoute);
app.use("/api/issues", issuesRoute);
app.use("/api/personal-infos", personalRoute);
app.use("/api/auth", authRoute);
app.use("/api/notifications", notificationRoute);
app.use("/api/plans", plansRoute);
app.use("/api/reviews", reviewsRoute);

// Start the server
const server = () => {
    db();
    app.listen(port, () => {
        console.log(`Server is running on port ${port}`);
    });
}

server()
