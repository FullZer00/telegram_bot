import datetime

from currency_converter import CurrencyConverter

from errors.validation_errors import MoreThanZeroError


class CurrencyService:
    def __init__(self, amount=0):
        self.amount = amount
        self.cur_converter = CurrencyConverter()

    def summa(self, value):
        try:
            self.amount = int(value)
        except:
            raise ValueError("Amount must be an integer.")
        if self.amount <= 0:
            self.amount = 0
            raise MoreThanZeroError("Amount must be greater than zero.")

    def convert(self, currency, new_currency):
        return round(self.cur_converter.convert(self.amount, currency, new_currency), 2)