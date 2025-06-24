from telebot import TeleBot
from telebot import types

class BaseCommand:
    def __init__(self, bot: TeleBot, name: str = 'main'):
        self.bot = bot
        self.name = name
        self.bot_states = set()
        self.start_message = None
        self.exit_message = None
        self.markup_exit = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        self.markup_exit.add(types.KeyboardButton("/exit"))

    def register(self):
        @self.bot.message_handler(commands=[self.name])
        def start(message):
            self.bot_states.add(message.chat.id)
            self.bot.send_message(message.chat.id, self.start_message, reply_markup=self.markup_exit)

        @self.bot.message_handler(commands=['exit'])
        def exit_bot(message):
            chat_id = message.chat.id
            if chat_id in self.bot_states:
                self.bot_states.remove(chat_id)
                self.bot.send_message(
                    chat_id,
                    self.exit_message,
                    reply_markup=types.ReplyKeyboardRemove()
            )