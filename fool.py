#!/usr/bin/env python2

"""fool - a dotfile sync toolkit"""
from __future__ import print_function

import argparse
import fool.git
import fool.xdg

def parse_args():
    args = argparse.ArgumentParser()
    args.add_argument('-c', '--config')
    return args.parse_args()

def main():
    args = parse_args()
    print(fool.git.which_git())
    xdg = fool.xdg.XDG()
    print(xdg.data_home)

if __name__ == '__main__':
    main()
