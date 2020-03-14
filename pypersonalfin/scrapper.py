from collections import defaultdict
from slugify import slugify
from itertools import chain

from utils.date import date_to_str
from utils.locale import is_brazil
from utils.amount import amount_to_str
from utils.file import get_files_of_data_folder, get_file_content

file_contents = None


def _get_file_contents():
    file_contents = {}

    data_files = chain(
        get_files_of_data_folder('*.txt'),
        get_files_of_data_folder('*.csv')
    )

    for file_path in data_files:
        file_name = file_path.name
        file_abs_path = file_path.absolute()

        file_contents[file_name] = get_file_content(file_abs_path)

    return file_contents


def _scrapper_parser(parser, locale, date_begin, date_end):
    global file_contents

    if not file_contents:
        file_contents = _get_file_contents()

    file_contents_of_parser = []
    for name, file_content in file_contents.items():
        if parser.match(name):
            file_contents_of_parser.append(file_content)

    return parser.get_categories(file_contents_of_parser, date_begin, date_end)


def _get_file_description(lower_bound_date, upper_bound_date, locale):
    name = "Data from {} to {}".format(
        date_to_str(lower_bound_date, locale),
        date_to_str(upper_bound_date, locale),
    )

    if is_brazil(locale):
        name = "Dados de {} ate {}".format(
            date_to_str(lower_bound_date, locale),
            date_to_str(upper_bound_date, locale),
        )

    return name


def _get_file_name_from_description(file_description):
    return slugify(file_description)


def scrapper(parserclasses, locale, date_begin, date_end):
    if not parserclasses or len(parserclasses) == 0:
        return

    categories_per_parser = defaultdict(list)
    amount = 0
    lower_bound_date = None
    upper_bound_date = None
    for parsercls in parserclasses:
        parser = parsercls(locale)
        parser_categories = _scrapper_parser(
            parser, locale, date_begin, date_end
        )

        for category in parser_categories:
            amount += category.amount
            if not lower_bound_date or lower_bound_date > category.lower_bound_date:
                lower_bound_date = category.lower_bound_date

            if not upper_bound_date or upper_bound_date < category.upper_bound_date:
                upper_bound_date = category.upper_bound_date

            categories_per_parser[parser.name].append(category)

    file_description = _get_file_description(
        lower_bound_date, upper_bound_date, locale
    )
    file_name = _get_file_name_from_description(file_description)

    csv = "{}\n".format(file_description)

    for parser_name, categories in categories_per_parser.items():
        categories.sort(key=lambda c: c.amount, reverse=True)

        csv += "\n{}:\n".format(parser_name)

        parser_amount = 0

        for category in categories:
            csv += "{}\n".format(category.to_csv())
            parser_amount += category.amount

        if is_brazil(locale):
            csv += "total {};{}\n".format(
                parser_name,
                amount_to_str(parser_amount, locale)
            )
        else:
            csv += "total {};{}\n".format(
                parser_name,
                amount_to_str(parser_amount, locale)
            )

    if is_brazil(locale):
        csv += "\nsaldo final;{}\n".format(amount_to_str(amount, locale))
    else:
        csv += "\ntotal balance;{}\n".format(amount_to_str(amount, locale))

    return (csv, file_name)
