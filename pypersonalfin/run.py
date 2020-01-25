#!/usr/bin/env python3
import sys

from persistors import persist_on_csv
from parsers import parsers
from scrapper import scrapper
from utils.locale import is_brazil
from utils.date import get_date_range
from utils.file import get_output_folder_abs_path


def _print_success(file_name, locale):
    file_path = get_output_folder_abs_path(file_name)

    if is_brazil(locale):
        print("Arquivo {}.csv gerado com sucesso".format(
            file_path
        ))
    else:
        print("Successful generated file {}.csv".format(
            file_path
        ))


def main(locale, begin, end):
    date_begin, date_end = get_date_range(begin, end)

    categories_csv, file_name = scrapper(parsers, locale, date_begin, date_end)

    persist_on_csv(categories_csv, file_name)

    _print_success(file_name, locale)

    if ".csv" not in file_name:
        file_name = "{}.csv".format(file_name)

    return file_name


if __name__ == "__main__":
    locale = 'en_us'
    if len(sys.argv) > 1:
        locale = sys.argv[1]

    main(locale, 'begin', 'end')
