from telebot import TeleBot
from telebot import types

class BaseCommand:
    def __init__(self, bot: TeleBot, name: str = 'main'):
        self.bot = bot
        self.name = name
        self.bot_states = set()
        self.start_message = f'Вход в режим {self.name}'
        self.exit_message = f'Выход из режима {self.name}'
        self.btn_exit = types.KeyboardButton("/exit")
        self.markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        self.markup.add(self.btn_exit)

    def register(self):
        @self.bot.message_handler(commands=[self.name])
        def start(message):
            self.bot_states.add(message.chat.id)
            self.handle_start(message)

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

    def handle_start(self, message):
        """Метод, который можно переопределять в подклассах"""
        self.bot.send_message(
            message.chat.id,
            self.start_message,
            reply_markup=self.markup
        )

    def _bot_send_message(self, chat_id, text, btns=None, **kwargs):
        if chat_id in self.bot_states:
            self.markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
            self._add_markup_buttons(btns)
            self.markup.add(self.btn_exit)
            kwargs.setdefault('reply_markup', self.markup)
        self.bot.send_message(chat_id, text, **kwargs)

    def _add_markup_buttons(self, btns):
        if btns:
            for btn in btns:
                if isinstance(btn, str):
                    self.markup.add(types.KeyboardButton(btn))
                elif isinstance(btn, types.KeyboardButton):
                    self.markup.add(btn)
                else:
                    raise TypeError("btn должен быть строкой или types.KeyboardButton")