#!/usr/bin/env python3
import sys


def main(locale):
    pass


if __name__ == "__main__":
    locale = 'en-us'
    if len(sys.argv) > 1:
        locale = sys.argv[1]

    main(locale)
