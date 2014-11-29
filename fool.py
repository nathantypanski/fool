#!/usr/bin/env python

"""fool - a dotfile sync toolkit"""
from __future__ import print_function

import argparse

import fool.cli

def main():
    parser = fool.cli.build_args()
    args = parser.parse_args()
    if 'func' in args:
        args.func(args)
    else:
        parser.print_help()

if __name__ == '__main__':
    main()
