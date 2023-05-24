const express = require('express');
const admin = require('firebase-admin');
require('dotenv').config();

const app = express();
app.use(express.json());

const serviceAccount = require('./path/to/serviceAccountKey.json'); // Update with your service account key

admin.initializeApp({
  credential: admin.credential.cert(serviceAccount),
  databaseURL: process.env.FIREBASE_DATABASE_URL,
});

const db = admin.database();

const checkApiKey = (req, res, next) => {
  const apiKey = req.headers['api-key'];
  if (apiKey === process.env.API_KEY) {
    req.isAuthorized = true;
  } else {
    req.isAuthorized = false;
  }
  next();
};

const hotelsRouter = require('./routes/hotels');
const roomsRouter = require('./routes/rooms');

app.use('/hotels', checkApiKey, hotelsRouter);
app.use('/hotels/:hotel_id/rooms', checkApiKey, roomsRouter);

const port = process.env.PORT || 3000;
app.listen(port, () => {
  console.log(`Server listening on port ${port}`);
});
