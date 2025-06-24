import os

from api.weather import WeatherApi
from commands.base_command import BaseCommand


class WeatherCommands(BaseCommand):
    def __init__(self, bot, name):
        super().__init__(bot, name)
        self.weatherAPI = WeatherApi()
        self.start_message = "Введите название города:"
        self.exit_message = "Выход из режима погоды"

    def register(self):
        super().register()
        @self.bot.message_handler(func=lambda message: message.chat.id in self.bot_states)
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
                            caption=self._format_temp_message(city, data),
                            reply_markup=self.markup_exit
                        )
                else:
                    self.bot.reply_to(message, self._format_temp_message(city, data))

            except Exception as e:
                print(e)
                self.bot.reply_to(message, f"Ошибка получения данных: {str(e)}")

    def _format_temp_message(self, city, data):
        return (f'Погода в {city} сейчас: {data["main"]["temp"]}℃\n'
                f'Минимум: {data["main"]["temp_min"]}℃\n'
                f'Максимум: {data["main"]["temp_max"]}℃')
