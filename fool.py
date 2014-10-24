#!/usr/bin/env python2

"""fool - a dotfile sync toolkit"""
from __future__ import print_function

import argparse
import os.path

import fool.conf
import fool.git
import fool.xdg

def config(args):
    if args.check:
        dirs = fool.conf.ConfigDirectories()
        out = 'config dir: {}\ndata dir: {}'.format(dirs.config_dir,
                                                    dirs.data_dir)
        print(out)

def parse_args():
    args = argparse.ArgumentParser()
    subs = args.add_subparsers(help='sub-command help')
    conf = subs.add_parser('config', help='configuration subsystem')
    conf.add_argument('--check',
                      action='store_true',
                      help='check the current fool configuration')
    conf.set_defaults(func=config)
    return args.parse_args()

def main():
    args = parse_args()
    args.func(args)

if __name__ == '__main__':
    main()
