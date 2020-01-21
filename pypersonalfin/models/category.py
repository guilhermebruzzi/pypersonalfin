from collections import defaultdict

from utils.amount import amount_to_str
from utils.locale import is_brazil


class Category:
    def __init__(self, name, locale):
        self.lower_bound_date = None
        self.upper_bound_date = None
        self.name = name.lower().strip()
        self.amount = 0
        self.statements = []
        self.locale = locale
        self.has_observation = False

    def append_statement(self, statement):
        if statement.category_name != self.name:
            return

        self.amount += statement.amount

        if not self.lower_bound_date or self.lower_bound_date > statement.date:
            self.lower_bound_date = statement.date

        if not self.upper_bound_date or self.upper_bound_date < statement.date:
            self.upper_bound_date = statement.date

        if statement.observation:
            self.has_observation = True

        self.statements.append(statement)

    def append_statements(self, statements, sort=False):
        if not statements or len(statements) == 0:
            return

        for statement in statements:
            self.append_statement(statement)

        if sort:
            self.statements.sort(key=lambda s: s.amount, reverse=True)

    def _get_csv_title(self):
        title = "*Category {}*".format(self.name)
        if is_brazil(self.locale):
            title = "*Categoria {}*".format(self.name)
        return "{}\n".format(title)

    def _get_csv_header(self):
        header = "date,title,amount"
        if self.has_observation:
            header += ",observation"

        return "{}\n".format(header)

    def to_csv(self):
        statements_csvs = [statement.to_csv() for statement in self.statements]

        csv = ""

        csv += self._get_csv_title()

        csv += self._get_csv_header()

        csv += "\n".join(statements_csvs)

        csv += "\ntotal,{}\n".format(amount_to_str(self.amount, self.locale))

        return csv

    def __str__(self):
        return self.to_csv()

    def __eq__(self, other):
        return self.name == other.name

    @classmethod
    def get_categories_from_statements(cls, statements, locale):
        if not statements or len(statements) == 0:
            return []

        memoize_statements_by_title = {}
        memoize_statements_by_category_name = defaultdict(list)
        for statement in statements:
            statement_title = statement.title.lower().strip()
            statement_category_name = statement.category_name.lower().strip()

            if statement_title in memoize_statements_by_title:
                saved_statement = memoize_statements_by_title[statement_title]
                saved_statement.amount += statement.amount
                if statement.date > saved_statement.date:
                    saved_statement.date = statement.date
            else:
                memoize_statements_by_title[statement_title] = statement
                memoize_statements_by_category_name[statement_category_name].append(
                    statement
                )

        categories = []
        for category_name, statements in memoize_statements_by_category_name.items():
            category = cls(category_name, locale)
            category.append_statements(statements, sort=True)
            categories.append(category)

        return categories
