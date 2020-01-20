from ..utils.amount import amount_to_str
from ..utils.date import convert_to_date


class Statement:
    def __init__(self, date, category_name, title, amount, locale):
        self.locale = locale
        self.date = convert_to_date(date, locale)
        self.category_name = category_name
        self.title = title
        self.amount = amount

    def to_csv(self):
        return amount_to_str(self.amount, self.locale)

    def __str__(self):
        return self.to_csv()
