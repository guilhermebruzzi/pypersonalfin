#!/usr/bin/env python3
import sys

from persistors import persist_on_csv
from parsers import parsers
from scrapper import scrapper
from utils.locale import is_brazil
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


def main(locale):
    categories_csv, file_name = scrapper(parsers, locale)

    persist_on_csv(categories_csv, file_name)

    _print_success(file_name, locale)


if __name__ == "__main__":
    locale = 'en-us'
    if len(sys.argv) > 1:
        locale = sys.argv[1]

    main(locale)
