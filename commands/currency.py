from typing import override

from telebot import types

from commands.base_command import BaseCommand
from errors.validation_errors import MoreThanZeroError
from services.currency_service import CurrencyService


class CurrencyCommands(BaseCommand):
    def __init__(self, bot, name):
        super().__init__(bot, name)
        self.cur_service = CurrencyService(0)
        self.btn_retry = types.KeyboardButton("🔁 Еще раз")

    def register(self):
        super().register()

        @self.bot.callback_query_handler(
            lambda call: '/' in call.data and call.message.chat.id in self.bot_states
        )
        def convert_default_callback(call):
            values = call.data.upper().split('/')
            self.convert(values, call.message.chat.id)


        @self.bot.callback_query_handler(
            func=lambda call: call.data == 'else' and call.message.chat.id in self.bot_states
        )
        def convert_else_callback(call):
            self._bot_send_message(call.message.chat.id, 'Введите название вакансий через слэш /')
            self.bot.register_next_step_handler(call.message, self.my_currency)


        @self.bot.callback_query_handler(
            func=lambda call: call.data == 'retry' and call.message.chat.id in self.bot_states
        )
        def retry_handler(call):
            self.bot.answer_callback_query(call.id)
            self.handle_start(call.message)

        @self.bot.message_handler(func=lambda message: message.text == '🔁 Еще раз')
        def retry_action(message):
            self.handle_start(message)

    @override
    def handle_start(self, message):
        self.bot.send_message(message.chat.id, 'Введите сумму')
        self.bot.register_next_step_handler(message, self.summa)

    def summa(self, message):
        amount = message.text.strip()
        try:
            self.cur_service.summa(amount)
        except ValueError:
            self.bot.send_message(message.chat.id, 'Неверный формат. Введите корректную сумму')
            self.bot.register_next_step_handler(message, self.summa)
            return
        except MoreThanZeroError:
            self.bot.send_message(message.chat.id, 'Сумма должна быть больше 0')
            self.bot.register_next_step_handler(message, self.summa)
            return

        markup = types.InlineKeyboardMarkup(row_width=2)
        btn1 = types.InlineKeyboardButton('USD/EUR', callback_data='usd/eur')
        btn2 = types.InlineKeyboardButton('EUR/USD', callback_data='eur/usd')
        btn3 = types.InlineKeyboardButton('USD/GBP', callback_data='usd/gbp')
        btn4 = types.InlineKeyboardButton('Другое значение', callback_data='else')
        markup.add(btn1, btn2, btn3, btn4)
        self.bot.send_message(message.chat.id, 'Выберите пару валют', reply_markup=markup)

    def my_currency(self, message):
        try:
            values = message.text.upper().split('/')
            self.convert(values, message.chat.id)
        except Exception as e:
            print(e)
            self._bot_send_message(message.chat.id, "Что-то не так. Впишите сумму заново")
            self.bot.register_next_step_handler(message, self.summa)

    def convert(self, values, chat_id):
        try:
            res = self.cur_service.convert(values[0], values[1])

            self._bot_send_message(
                chat_id,
                f'Вывод: {res} {values[1]}',
                btns=[self.btn_retry],
            )
        except Exception as e:
            self._bot_send_message(chat_id, f"Ошибка: {str(e)}", btns=[self.btn_retry])
            raise e
