#!/usr/bin/env python3

""" fool - a dotfile sync toolkit """

import argparse
import sys
import fool.git

def parse_args():
    args = argparse.ArgumentParser()
    args.add_argument('-c', '--config')
    return args.parse_args()

def main():
    args = parse_args()
    print(fool.git.which_git())

if __name__ == '__main__':
    main()
