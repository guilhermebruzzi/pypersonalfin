from ..models.category import Category
from ..models.statement import Statement


def prefix_file_name(file_name):
    file_name


class BaseParser:
    def __init__(self, name):
        self.name = name

    def match(self, file_name):
        return prefix_file_name(file_name).lower() == self.name.lower()

    def get_categories(self, file_contents):
        statements = [
            self.get_statement(data) for data in file_content.split('\n') for file_content in file_contents
        ]
        return Category.get_categories_from_statements(statements)

    def get_statement(self, data):
        return
