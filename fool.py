#!/usr/bin/env python

"""fool - a dotfile sync toolkit"""
from __future__ import print_function

import argparse

import fool.conf
import fool.group
import fool.xdg

def fool_config_check(args):
    dirs = fool.conf.ConfigDirectories()
    print('config dir: {}\ndata dir: {}'.format(dirs.config_dir,
                                                dirs.data_dir))

def fool_group_init(args):
    group_list = fool.group.GroupListConfig.from_config_file()
    print('Creating new group {}'.format(args.name))
    grp = fool.group.Group(args.name, args.source, args.dest)
    print(grp)
    group_list.add(grp)
    group_list.write()


def fool_group_rm(args):
    group_list = fool.group.GroupListConfig.from_config_file()
    print('Removing group {}'.format(args.name))
    group_list.discard(args.name)
    group_list.write()
    print('success')


def fool_group_list(args):
    group_list = fool.group.GroupListConfig.from_config_file()
    print(group_list.groups)


def build_args():
    xdg_config = fool.xdg.XDGConfig()
    parent_parser = argparse.ArgumentParser(add_help=False)
    main_parser = argparse.ArgumentParser()
    service_subparsers = main_parser.add_subparsers(title='service',
                                                    dest='service_command')
    group_parser = service_subparsers.add_parser('group',
                                                 help='fool groups',
                                                 parents=[parent_parser])
    group_subparser = group_parser.add_subparsers(title='group actions',
                                                  dest='action_command')
    group_list = group_subparser.add_parser('list', help='show known groups',
                                            parents=[parent_parser])
    group_list.set_defaults(func=fool_group_list)
    group_init = group_subparser.add_parser('init', help='create a new group',
                                            parents=[parent_parser])
    group_init.add_argument('name', help='name of group')
    group_init.add_argument('-s', '--source', help='source folder for group')
    group_init.add_argument('-d', '--dest', help='destination folder for group',
                            default=xdg_config.home)
    group_init.set_defaults(func=fool_group_init)
    group_init = group_subparser.add_parser('rm', help='remove a group',
                                            parents=[parent_parser])
    group_init.add_argument('name', help='name of group')
    group_init.set_defaults(func=fool_group_rm)
    config_parser = service_subparsers.add_parser('config', help='fool config',
                                                  parents=[parent_parser])
    config_subparser = config_parser.add_subparsers(title='conf actions',
                                                    dest='action_command')
    config_check = config_subparser.add_parser('check',
                                               help='show the configuration')
    config_check.set_defaults(func=fool_config_check)
    return main_parser

def main():
    parser = build_args()
    args = parser.parse_args()
    if 'func' in args:
        args.func(args)
    else:
        parser.print_help()

if __name__ == '__main__':
    main()
