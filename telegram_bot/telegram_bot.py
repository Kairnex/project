
import logging
import requests
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
from web3 import Web3

# Your bot token from BotFather
TELEGRAM_BOT_TOKEN = 'YOUR_BOT_TOKEN'

# Backend API URL
API_URL = "http://your-vps-ip:5000"

# Ethereum setup (Infura or your provider URL)
WEB3_PROVIDER_URL = 'https://mainnet.infura.io/v3/YOUR_INFURA_PROJECT_ID'  # Use your Infura/Alchemy URL here
w3 = Web3(Web3.HTTPProvider(WEB3_PROVIDER_URL))

# Initialize Updater and Dispatcher
updater = Updater(TELEGRAM_BOT_TOKEN, use_context=True)
dispatcher = updater.dispatcher

# Set up logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Command to start the bot
def start(update: Update, context: CallbackContext):
    update.message.reply_text("Welcome to HamsterHub! Use /help to see available commands.")

# Command to check balance
def balance(update: Update, context: CallbackContext):
    telegram_id = update.message.from_user.id
    response = requests.get(f'{API_URL}/balance/{telegram_id}')
    data = response.json()
    if 'balance' in data:
        update.message.reply_text(f'Your current balance: {data["balance"]} AU')
    else:
        update.message.reply_text("Error: Could not fetch balance.")

# Command to get referral code
def referral(update: Update, context: CallbackContext):
    telegram_id = update.message.from_user.id
    response = requests.get(f'{API_URL}/referral/{telegram_id}')
    data = response.json()
    if 'referralCode' in data:
        update.message.reply_text(f"Your referral code: {data['referralCode']}
Share it with your friends!")
    else:
        update.message.reply_text("Error: Could not fetch referral code.")

# Command to tap and earn tokens
def tap(update: Update, context: CallbackContext):
    telegram_id = update.message.from_user.id
    response = requests.post(f'{API_URL}/tap/{telegram_id}')
    data = response.json()
    if 'success' in data and data['success']:
        update.message.reply_text(f"You earned 1 AU token! New balance: {data['balance']} AU")
    else:
        update.message.reply_text("Error: Could not process your tap.")

# Help command
def help(update: Update, context: CallbackContext):
    update.message.reply_text(
        "/start - Start the bot
"
        "/balance - Check your token balance
"
        "/referral - Get your referral code
"
        "/tap - Tap to earn tokens"
    )

# Add command handlers
dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(CommandHandler("balance", balance))
dispatcher.add_handler(CommandHandler("referral", referral))
dispatcher.add_handler(CommandHandler("tap", tap))
dispatcher.add_handler(CommandHandler("help", help))

# Start the bot
updater.start_polling()
updater.idle()
