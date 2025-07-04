import os

import telebot
from dotenv import load_dotenv

from commands.currency import CurrencyCommands
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

userCommands = UsersCommands(db_manager, bot, name='user')
userCommands.register()

weatherCommands = WeatherCommands(bot, name='weather')
weatherCommands.register()

currencyCommands = CurrencyCommands(bot, name='currency')
currencyCommands.register()

bot.infinity_polling()
