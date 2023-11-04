from telegram import Bot
import os

telegram_bot_token = os.environ["TELEGRAMTOKEN"]
bot = Bot(telegram_bot_token)