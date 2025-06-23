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

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Приветствую вас. Надеюсь я смогу вам как-то помочь)")

userCommands = UsersCommands(db_manager, bot)
userCommands.register()

weatherCommands = WeatherCommands(bot)
weatherCommands.register()

bot.infinity_polling()
