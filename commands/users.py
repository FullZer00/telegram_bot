from telebot import types

from commands.base_command import BaseCommand

class UsersCommands(BaseCommand):
    def __init__(self, db_manager, bot, name):
        super().__init__(bot, name)
        self.__db = db_manager
        self.__name = None

    def register(self):
        super().register()
        @self.bot.message_handler(commands=['register'], func=lambda message: message.chat.id in self.bot_states)
        def register(message):
            self._bot_send_message(message.chat.id, 'Привет, сейчас тебя зарегистрируем. Введи свое имя')
            self.bot.register_next_step_handler(message, self.user_name)

        @self.bot.callback_query_handler(func=lambda call: call.message.chat.id in self.bot_states)
        def callback(call):
            info = self.users_info()
            self.bot.send_message(call.message.chat.id, info)

        @self.bot.message_handler(commands=['users'], func=lambda message: message.chat.id in self.bot_states)
        def users(message):
            info = self.users_info()
            self._bot_send_message(message.chat.id, info)

    def user_name(self, message):
        self.__name = message.text.strip()
        self._bot_send_message(message.chat.id, 'Введите пароль')
        self.bot.register_next_step_handler(message, self.user_pass)

    def user_pass(self, message):
        password = message.text.strip()

        self.__db.add_user(self.__name, password)

        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("Список пользователей", callback_data='users'))
        self._bot_send_message(message.chat.id, 'Пользователь зарегистрирован', reply_markup=markup)
        # bot.register_next_step_handler(message, user_pass)

    def user_list(self):
        users = self.__db.get_all_users()

        return users

    def users_info(self):
        users = self.user_list()
        info = ''
        for user in users:
            info += f'Имя: {user[1]}\n'

        return info
