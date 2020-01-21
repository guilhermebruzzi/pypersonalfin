#!/usr/bin/env python3
import sys

from persistors import persist_on_csv
from parsers import parsers
from scrapper import scrapper


def main(locale):
    categories_csv, file_name = scrapper(parsers, locale)

    persist_on_csv(categories_csv, file_name)


if __name__ == "__main__":
    main(sys.argv[1])
