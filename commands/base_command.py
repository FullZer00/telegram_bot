class BaseCommand:
    def __init__(self, bot):
        self.bot = bot

    def register(self):
        raise NotImplementedError