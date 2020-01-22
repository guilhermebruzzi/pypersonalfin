from utils.date import date_to_str
from utils.locale import is_brazil
from utils.amount import amount_to_str

file_contents = None


def _get_file_contents():
    return {
        "nubank-2020-01": "date,category,title,amount\n2019-11-28,,Rewards - Assinatura,190",
        "itau-2020-01": "22/11/2019;RSHOP-SURREAL RES-22/11;-95,70\n22/11/2019;TBI 0413.67950-7     C/C;-300,00",
    }


def _scrapper_parser(parsercls, locale):
    global file_contents

    parser = parsercls(locale)

    if not file_contents:
        file_contents = _get_file_contents()

    file_contents_of_parser = []
    for name, file_content in file_contents.items():
        if parser.match(name):
            file_contents_of_parser.append(file_content)

    return parser.get_categories(file_contents_of_parser)


def _get_file_name(lower_bound_date, upper_bound_date, locale):
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


def scrapper(parserclasses, locale):
    if not parserclasses or len(parserclasses) == 0:
        return

    categories = []
    amount = 0
    lower_bound_date = None
    upper_bound_date = None
    for index, parsercls in enumerate(parserclasses):
        parser_categories = _scrapper_parser(parsercls, locale)
        for category in parser_categories:
            amount += category.amount
            if not lower_bound_date or lower_bound_date > category.lower_bound_date:
                lower_bound_date = category.lower_bound_date

            if not upper_bound_date or upper_bound_date < category.upper_bound_date:
                upper_bound_date = category.upper_bound_date

            categories.append(category)

    categories.sort(key=lambda c: c.amount, reverse=True)

    file_name = _get_file_name(lower_bound_date, upper_bound_date, locale)

    csv = "{}\n".format(file_name)

    categories_csv = [category.to_csv() for category in categories]

    csv += '\n'.join(categories_csv)

    csv += "\ntotal,{}\n".format(amount_to_str(amount, locale))

    return (csv, file_name)
