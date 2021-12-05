from utils.amount import amount_to_str
from utils.date import convert_to_date, date_to_str


class Statement:
    def __init__(self, date, category_name, title, amount, locale, observation=None):
        self.locale = locale
        self.date = convert_to_date(date, locale)
        self.category_name = category_name
        self.title = title
        self.amount = amount
        self.observation = observation

    def to_csv(self):
        amount = amount_to_str(self.amount, self.locale)
        date = date_to_str(self.date, self.locale)
        csv = "{};{};{};{}".format(
            date, self.title, self.category_name, amount)

        if self.observation:
            csv += ";{}".format(self.observation)

        return csv

    def __str__(self):
        return self.to_csv()
