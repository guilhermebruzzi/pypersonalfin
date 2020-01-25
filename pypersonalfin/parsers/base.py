from models.category import Category
from models.statement import Statement
from utils.locale import is_brazil


def prefix_file_name(file_name):
    if not file_name:
        return ''

    name = file_name.split('.')[0]
    return name.split('-')[0]


class BaseParser:
    def __init__(self, name, locale, statement_separator=','):
        self.name = name
        self.locale = locale
        self.statement_separator = statement_separator

    def _get_default_category_name(self, amount=0):
        if amount == 0:
            return 'vazia' if is_brazil(self.locale) else 'blank'
        if amount < 0:
            return 'saida' if is_brazil(self.locale) else 'exit'
        return 'entrada' if is_brazil(self.locale) else 'income'

    def get_amount(self, amount):
        try:
            amount = amount.strip()
            if is_brazil(self.locale):
                amount = amount.replace(',', '.')
            amount = float(amount) * 100
            amount = int(amount)
        except ValueError:
            pass
        except AttributeError:
            pass

        return amount

    def get_statement(self, data):
        data_values = data.split(self.statement_separator)

        category_name = None

        if len(data_values) == 3:
            date, title, amount = data_values
        elif len(data_values) == 4:
            date, category_name, title, amount = data_values
        else:
            amount = None

        amount = self.get_amount(amount)

        if not isinstance(amount, int):
            return None

        if not category_name:
            category_name = self._get_default_category_name(amount)

        return Statement(date, category_name, title, amount, self.locale)

    def match(self, file_name):
        return prefix_file_name(file_name).lower() == self.name.lower()

    def get_categories(self, file_contents, date_begin, date_end):
        statements = []

        for file_content in file_contents:
            for data in file_content.split('\n'):
                statement = self.get_statement(data)
                if statement:
                    statements.append(statement)

        return Category.get_categories_from_statements(statements, self.locale, date_begin, date_end)
