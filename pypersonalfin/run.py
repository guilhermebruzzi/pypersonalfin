#!/usr/bin/env python3

import sys

def main(args):
    print('hello world')
    for arg in args:
        print(arg)

main(sys.argv[1:])
