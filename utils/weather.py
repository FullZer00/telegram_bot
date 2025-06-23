from pathlib import Path


class WeatherHelper:
    ASSETS_DIR = Path(__file__).parent.parent / 'assets' / 'img'
    WEATHER_IMAGES = {
        'Clear': 'sun.png',
        'Clouds': 'cloudy.png',
        'Rain': 'rain.png',
        'default': 'dull.png'
    }

    @classmethod
    def get_path_icon_weather(cls, weather_main):
        if weather_main == 'Clear':
            icon = str(cls.ASSETS_DIR / 'sun.png')
        elif weather_main == 'Clouds':
            icon = str(cls.ASSETS_DIR / 'cloudy.png')
        elif weather_main == 'Rain':
            icon = str(cls.ASSETS_DIR / 'rain.png')
        else:
            icon = str(cls.ASSETS_DIR / 'dull.png')

        return icon


