from telebot import types

from commands.base_command import BaseCommand


class UsersCommands(BaseCommand):
    def __init__(self, db_manager, bot):
        super().__init__(bot)
        self.db = db_manager
        self.name = None

    def register(self):
        @self.bot.message_handler(commands=['start'])
        def start(message):
            self.bot.send_message(message.chat.id, 'Привет, сейчас тебя зарегистрируем. Введи свое имя.')
            self.bot.register_next_step_handler(message, self.user_name)

        @self.bot.callback_query_handler(func=lambda call: True)
        def callback(call):
            users = self.user_list()
            info = ''
            for user in users:
                info += f'Имя: {user[1]}\n'

            self.bot.send_message(call.message.chat.id, info)

    def user_name(self, message):
        self.name = message.text.strip()
        self.bot.send_message(message.chat.id, 'Введите пароль')
        self.bot.register_next_step_handler(message, self.user_pass)

    def user_pass(self, message):
        password = message.text.strip()

        self.db.add_user(self.name, password)

        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("Список пользователей", callback_data='users'))
        self.bot.send_message(message.chat.id, 'Пользователь зарегистрирован', reply_markup=markup)
        # bot.register_next_step_handler(message, user_pass)

    def user_list(self):
        users = self.db.get_all_users()

        return users