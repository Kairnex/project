
const express = require('express');
const Web3 = require('web3');
const mongoose = require('mongoose');
const cors = require('cors');
const bodyParser = require('body-parser');
const app = express();
const port = 5000;

// Use JSON body parsing and enable CORS for cross-origin requests
app.use(bodyParser.json());
app.use(cors());

// MongoDB setup
mongoose.connect(process.env.MONGO_URI, { useNewUrlParser: true, useUnifiedTopology: true });

// Web3 setup (Replace with your Web3 provider URL)
const web3 = new Web3(new Web3.providers.HttpProvider(process.env.INFURA_URL));

// Define a simple User model for MongoDB
const User = mongoose.model('User', new mongoose.Schema({
  telegramId: String,
  balance: Number,
  referralCode: String,
  referredBy: String,
}));

// Endpoint to get balance
app.get('/balance/:telegramId', async (req, res) => {
  const user = await User.findOne({ telegramId: req.params.telegramId });
  if (user) {
    res.json({ balance: user.balance });
  } else {
    res.status(404).json({ message: 'User not found' });
  }
});

// Endpoint to increment balance when user taps
app.post('/tap/:telegramId', async (req, res) => {
  const user = await User.findOne({ telegramId: req.params.telegramId });
  if (user) {
    user.balance += 1; // Increment balance by 1 AU
    await user.save();
    res.json({ success: true, balance: user.balance });
  } else {
    res.status(404).json({ message: 'User not found' });
  }
});

// Endpoint to get referral code
app.get('/referral/:telegramId', async (req, res) => {
  const user = await User.findOne({ telegramId: req.params.telegramId });
  if (user) {
    res.json({ referralCode: user.referralCode });
  } else {
    res.status(404).json({ message: 'User not found' });
  }
});

// Start the server
app.listen(port, () => {
  console.log(`Backend running on http://localhost:${port}`);
});
