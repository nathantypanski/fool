"""Command-line interface.
"""

import argparse

import fool.conf
import fool.xdg


def fool_config_check(args):
    dirs = fool.conf.ConfigDirectories()
    print('config dir: {}\ndata dir: {}'.format(dirs.config_dir,
                                                dirs.data_dir))

def fool_chapter_init(args):
    chapter_list = fool.chapter.ChapterListConfig.from_config_file()
    print('Creating new chapter {}'.format(args.name))
    grp = fool.chapter.Chapter(args.name, args.source, args.dest)
    print(grp)
    chapter_list.add(grp)
    chapter_list.write()


def fool_chapter_rm(args):
    chapter_list = fool.chapter.ChapterListConfig.from_config_file()
    print('Removing chapter {}'.format(args.name))
    chapter_list.discard(args.name)
    chapter_list.write()
    print('success')


def fool_chapter_list(args):
    chapter_list = fool.chapter.ChapterListConfig.from_config_file()
    print(chapter_list.chapters)


def build_args():
    xdg_config = fool.xdg.XDGConfig()
    parent_parser = argparse.ArgumentParser(add_help=False)
    main_parser = argparse.ArgumentParser()
    service_subparsers = main_parser.add_subparsers(title='service',
                                                    dest='service_command')
    chapter_parser = service_subparsers.add_parser('chapter',
                                                 help='fool chapters',
                                                 parents=[parent_parser])
    chapter_subparser = chapter_parser.add_subparsers(title='chapter actions',
                                                  dest='action_command')
    chapter_list = chapter_subparser.add_parser('list', help='show known chapters',
                                            parents=[parent_parser])
    chapter_list.set_defaults(func=fool_chapter_list)
    chapter_init = chapter_subparser.add_parser('init', help='create a new chapter',
                                            parents=[parent_parser])
    chapter_init.add_argument('name', help='name of chapter')
    chapter_init.add_argument('-s', '--source', help='source folder for chapter')
    chapter_init.add_argument('-d', '--dest', help='destination folder for chapter',
                            default=xdg_config.home)
    chapter_init.set_defaults(func=fool_chapter_init)
    chapter_init = chapter_subparser.add_parser('rm', help='remove a chapter',
                                            parents=[parent_parser])
    chapter_init.add_argument('name', help='name of chapter')
    chapter_init.set_defaults(func=fool_chapter_rm)
    config_parser = service_subparsers.add_parser('config', help='fool config',
                                                  parents=[parent_parser])
    config_subparser = config_parser.add_subparsers(title='conf actions',
                                                    dest='action_command')
    config_check = config_subparser.add_parser('check',
                                               help='show the configuration')
    config_check.set_defaults(func=fool_config_check)
    return main_parser
