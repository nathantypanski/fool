#!/usr/bin/env python2

"""fool - a dotfile sync toolkit"""
from __future__ import print_function

import argparse
import sys

import fool.conf
import fool.git
import fool.xdg

def fool_config_check(args):
    dirs = fool.conf.ConfigDirectories()
    print('config dir: {}\ndata dir: {}'.format(dirs.config_dir,
                                                dirs.data_dir))

def fool_group_init(args):
    print('Creating new group {}'.format(args.name))
    print('    source: {}'.format(args.source))
    print('    dest: {}'.format(args.dest))

def parse_args():
    xdg_config = fool.xdg.XDGConfig()
    parent_parser = argparse.ArgumentParser(add_help=False)
    main_parser = argparse.ArgumentParser()
    service_subparsers = main_parser.add_subparsers(title='service', dest='service_command')
    group_parser = service_subparsers.add_parser('group', help='fool groups', parents=[parent_parser])
    group_subparser = group_parser.add_subparsers(title='group actions', dest='action_command')
    group_init = group_subparser.add_parser('init', help='create a new group',
                        parents=[parent_parser])
    group_init.add_argument('name', help='name of group')
    group_init.add_argument('-s', '--source', help='source folder for group')
    group_init.add_argument('-d', '--dest', help='destination folder for group',
                            default=xdg_config.home)
    group_init.set_defaults(func=fool_group_init)
    conf_parser = service_subparsers.add_parser('config', help='fool config', parents=[parent_parser])
    conf_subparser = conf_parser.add_subparsers(title='conf actions', dest='action_command')
    conf_check = conf_subparser.add_parser('check', help='show the configuration')
    conf_check.set_defaults(func=fool_config_check)
    return main_parser.parse_args()

def main():
    args = parse_args()
    args.func(args)

if __name__ == '__main__':
    main()
