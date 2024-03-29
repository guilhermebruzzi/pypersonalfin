from collections import defaultdict
from slugify import slugify

from utils.locale import is_brazil


class Category:
    def __init__(self, name, locale, date_begin=None, date_end=None):
        self.name = name.lower().strip()
        self.locale = locale
        self.date_begin = date_begin
        self.date_end = date_end
        self.lower_bound_date = None
        self.upper_bound_date = None
        self.amount = 0
        self.statements = []
        self.has_observation = False

    def append_statement(self, statement):
        if statement.category_name != self.name:
            return

        if self.date_begin and self.date_end and (statement.date < self.date_begin or statement.date > self.date_end):
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

    def csv_header(self):
        header = "date;title;category;amount"
        if is_brazil(self.locale):
            header = "data;titulo;categoria;valor"

        if self.has_observation:
            if is_brazil(self.locale):
                header += ";observacao"
            else:
                header += ";observation"

        return "{}\n".format(header)

    def is_empty(self):
        return len(self.statements) == 0

    def to_csv(self):
        self.statements.sort(key=lambda c: c.date)
        statements_csvs = [statement.to_csv() for statement in self.statements]

        return "\n".join(statements_csvs)

    def __str__(self):
        return self.to_csv()

    def __eq__(self, other):
        return self.name == other.name

    @classmethod
    def get_default_category_name(cls, amount, locale):
        if amount == 0:
            return 'vazia' if is_brazil(locale) else 'blank'
        if amount < 0:
            return 'saida' if is_brazil(locale) else 'exit'
        return 'entrada' if is_brazil(locale) else 'income'

    @classmethod
    def get_categories_from_statements(cls, statements, locale, date_begin, date_end):
        if not statements or len(statements) == 0:
            return []

        memoize_statements_by_title_slug = {}
        memoize_statements_by_category_name_slug = defaultdict(list)
        for statement in statements:
            statement_title_slug = slugify(statement.title.lower().strip())
            statement_category_name = statement.category_name.lower().strip()
            statement_category_name_slug = slugify(statement_category_name)

            if statement_title_slug in memoize_statements_by_title_slug:
                saved_statement_index = memoize_statements_by_title_slug[statement_title_slug][1]
                memoize_statements_by_category_name_slug[statement_category_name_slug].insert(
                    saved_statement_index,
                    statement
                )
            else:
                memoize_statements_by_title_slug[statement_title_slug] = [statement, len(
                    memoize_statements_by_category_name_slug[statement_category_name_slug])]
                memoize_statements_by_category_name_slug[statement_category_name_slug].append(
                    statement
                )

        categories = []
        for statements in memoize_statements_by_category_name_slug.values():
            if len(statements) == 0:
                continue

            category_name = statements[0].category_name.lower().strip()
            category = cls(category_name, locale, date_begin, date_end)
            category.append_statements(statements, sort=True)

            if category.is_empty():
                continue

            categories.append(category)

        return categories
