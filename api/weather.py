import json
import os
import requests

from errors.api_errors import ApiError
from utils.weather import WeatherHelper


class WeatherApi:
    def __init__(self):
        self.__API_KEY = os.getenv('WEATHER_API_KEY')

    def get_temp_city(self, city: str):
        try:
            res = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={self.__API_KEY}&units=metric')
            if res.status_code == 200:
                data = json.loads(res.text)
                weather = data['weather'][0]['main']
                data['img'] = WeatherHelper.get_path_icon_weather(weather)
                return data
            else:
                raise ApiError("Город указан неверно")
        except requests.exceptions.RequestException as e:
            raise e

