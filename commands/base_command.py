from telebot import TeleBot


class BaseCommand:
    def __init__(self, bot: TeleBot):
        self.bot = bot

    def register(self):
        raise NotImplementedError