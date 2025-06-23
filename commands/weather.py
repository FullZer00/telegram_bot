import os

from api.weather import WeatherApi
from commands.base_command import BaseCommand
from telebot import types


class WeatherCommands(BaseCommand):
    def __init__(self, bot):
        super().__init__(bot)
        self.weatherAPI = WeatherApi()
        self.weather_states = set()

    def register(self):
        @self.bot.message_handler(commands=['weather'])
        def weather(message):
            self.weather_states.add(message.chat.id)
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
            markup.add(types.KeyboardButton("/exit"))
            self.bot.send_message(message.chat.id, "Напиши название города", reply_markup=markup)

        @self.bot.message_handler(commands=['exit'])
        def exit_weather(message):
            chat_id = message.chat.id
            if chat_id in self.weather_states:
                self.weather_states.remove(chat_id)
                self.bot.send_message(
                    chat_id,
                    "Режим погоды отменён",
                    reply_markup=types.ReplyKeyboardRemove()
                )

        @self.bot.message_handler(content_types=['text'])
        def get_weather(message):
            city = message.text.strip()
            try:
                data = self.weatherAPI.get_temp_city(city.lower())

                # Проверяем существование файла перед отправкой
                if os.path.exists(data["img"]):
                    with open(data["img"], 'rb') as img_file:
                        self.bot.send_photo(
                            chat_id=message.chat.id,
                            photo=img_file,
                            caption=f'Погода в {city} сейчас: {data["main"]["temp"]}℃\n'
                                    f'Минимум: {data["main"]["temp_min"]}℃\n'
                                    f'Максимум: {data["main"]["temp_max"]}℃'
                        )
                else:
                    self.bot.reply_to(message,
                                      f'Погода в {city} сейчас: {data["main"]["temp"]}℃\n'
                                      f'Минимум: {data["main"]["temp_min"]}℃\n'
                                      f'Максимум: {data["main"]["temp_max"]}℃')

            except Exception as e:
                print(e)
                self.bot.reply_to(message, f"Ошибка получения данных: {str(e)}")
