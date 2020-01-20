file_contents = None


def _get_file_contents():
    return {
        "nubank-2020-01": "date,category,title,amount\n2019-11-28,,Rewards - Assinatura,190",
        "itau-2020-01": "22/11/2019;RSHOP-SURREAL RES-22/11;-95,70\n22/11/2019;TBI 0413.67950-7     C/C;-300,00",
    }


def scrapper(parser):
    if not parser:
        return

    if not file_contents:
        file_contents = _get_file_contents()

    file_contents_of_parser = [
        file_content for name, file_content in file_contents.items() if parser.match(name)
    ]

    return parser.get_categories(file_contents_of_parser)
