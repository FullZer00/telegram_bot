import os
import webbrowser

import telebot
from dotenv import load_dotenv
from telebot import types

from consts import Sites

load_dotenv()

token = os.getenv('TELEGRAM_BOT_TOKEN')

bot = telebot.TeleBot(token)


@bot.message_handler(commands=['site', 'website'])
def site(message):
    webbrowser.open(os.getenv('GH_REPO'))


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, f'Привет {message.from_user.first_name}')


@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat.id, 'Здесь будет <b>информация</b> о <em>боте</em>...', parse_mode='HTML')


@bot.message_handler(content_types=['photo'])
def get_photo(message):
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton('Перейти на сайт', url=Sites.REPO)
    btn2 = types.InlineKeyboardButton('Удалить фото', callback_data='delete')
    btn3 = types.InlineKeyboardButton('Изменить текст', callback_data='edit')
    markup.row(btn1)
    markup.add(btn2, btn3)
    bot.reply_to(message, 'Какое красивое фото!', reply_markup=markup)


@bot.callback_query_handler(func=lambda callback: True)
def callback_message(callback):
    if callback.data == 'delete':
        bot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.message_id - 1)
    elif callback.data == 'edit':
        bot.edit_message_text('Edit text', chat_id=callback.message.chat.id, message_id=callback.message.message_id)


@bot.message_handler()
def info(message):
    if message.text.lower() == 'привет':
        start(message)
    elif message.text.lower() == 'id':
        bot.reply_to(message, f'ID: {message.from_user.id}')


bot.infinity_polling()
