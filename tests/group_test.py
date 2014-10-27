"""fool group test suite"""

import unittest
import os

try:
    import ConfigParser
    configparser = ConfigParser
except ImportError:
    import configparser

import fool.group
import util

class UnitTest(unittest.TestCase):

    def test_group_with_name_and_path(self):
        with util.temporary_config() as xdg_config:
            group_config = fool.group.GroupConfig()
            group_source = xdg_config.home / 'test'
            grp = fool.group.Group('Group', group_source)
            self.assertEqual(grp.name, 'Group')
            self.assertEqual(grp.source, group_source)
            group_config.add(grp)
            self.assertTrue(grp in group_config)
            self.assertTrue(grp.name in group_config)

    def test_create_group_from_iterable(self):
        with util.temporary_config() as xdg_config:
            grp_a_src = xdg_config.home / 'a'
            grp_a = fool.group.Group('grpa', grp_a_src)
            grp_b_src = os.path.join(xdg_config.home, 'b')
            grp_b = fool.group.Group('grpb', grp_a_src)
            group_config = fool.group.GroupConfig([grp_a, grp_b])
            self.assertEqual(len(group_config), 2)
            self.assertEqual(group_config['grpa'], grp_a)
            self.assertEqual(group_config['grpb'], grp_b)

    def test_write_one_group_to_file(self):
        with util.temporary_config() as xdg_config:
            group_source = xdg_config.home / 'test'
            grp = fool.group.Group('Group', group_source)
            group_config = fool.group.GroupConfig([grp])
            group_config.write()
            config_parser = configparser.SafeConfigParser()
            config_parser.read(str(group_config.path))
            group_config.clear_state()
            group_config = fool.group.GroupConfig()
            self.assertEqual(len(group_config), 0)
            group_config = group_config.from_config_file(config_parser)
            self.assertEqual(group_config['Group'].source, group_source)
            self.assertEqual(group_config['Group'].destination, xdg_config.home)

    def test_walk_group_files(self):
        with util.temporary_config() as xdg_config:
            group_source = xdg_config.home / 'test'
            os.mkdir(str(group_source))
