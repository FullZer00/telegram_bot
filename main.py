import os

import telebot
from dotenv import load_dotenv

from commands.users import UsersCommands
from commands.weather import WeatherCommands
from database.database_manager import DatabaseManager

load_dotenv()

token = os.getenv('TELEGRAM_BOT_TOKEN')

bot = telebot.TeleBot(token)

db_manager = DatabaseManager()

userCommands = UsersCommands(db_manager, bot)
userCommands.register()

weatherCommands = WeatherCommands(bot)
weatherCommands.register()

bot.infinity_polling()
