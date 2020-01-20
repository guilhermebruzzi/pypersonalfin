from ..utils.amount import amount_to_str


class Category:
    def __init__(self, name, locale):
        self.lower_bound_date = None
        self.upper_bound_date = None
        self.name = name.lower().strip()
        self.amount = 0
        self.statements = []
        self.locale = locale

    def append_statement(self, statement):
        if statement.category_name != self.name:
            return

        self.amount += statement.amount

        if not self.lower_bound_date or self.lower_bound_date > statement.date:
            self.lower_bound_date = statement.date

        if not self.upper_bound_date or self.upper_bound_date < statement.date:
            self.upper_bound_date = statement.date

        self.statements.append(statement)

    def to_csv(self):
        statements_csvs = [statement.to_csv() for statement in self.statements]

        csv = "date,category,title,amount\n"

        csv += "\n".join(statements_csvs)

        csv += "total,{}\n".format(amount_to_str(self.amount, self.locale))

        return csv

    def __str__(self):
        return self.to_csv()

    def __eq__(self, other):
        return self.name == other.name

    @classmethod
    def get_categories_from_statements(cls, statements):
        return cls()
