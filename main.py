import telebot
import os
from dotenv import load_dotenv
import webbrowser

load_dotenv()

token = os.getenv('TELEGRAM_BOT_TOKEN')

bot = telebot.TeleBot(token)

@bot.message_handler(commands=['site, website'])
def site(message):
    webbrowser.open('')

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, f'Привет {message.from_user.first_name}')

@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat.id, 'Здесь будет <b>информация</b> о <em>боте</em>...', parse_mode='HTML')

@bot.message_handler()
def info(message):
    if message.text.lower() == 'привет':
        start(message)
    elif message.text.lower() == 'id':
        bot.reply_to(message, f'ID: {message.from_user.id}')

bot.infinity_polling()