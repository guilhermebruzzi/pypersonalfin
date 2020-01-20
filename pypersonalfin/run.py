#!/usr/bin/env python3
from .parsers import parsers
from .scrapper import scrapper
from .persistors import persist_on_csv


def main():
    categories = [
        category for parser in parsers for category in scrapper(parser)
    ]
    persist_on_csv(categories)


if __name__ == "__main__":
    main()
