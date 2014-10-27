"""fool group test suite"""

from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals

import unittest
import os

from six.moves import configparser
from six.moves import map

import fool.group
import tests.util

class UnitTest(unittest.TestCase):

    def test_group_with_name_and_path(self):
        with tests.util.temporary_config() as xdg_config:
            group_config = fool.group.GroupListConfig()
            group_source = xdg_config.home / 'test'
            grp = fool.group.Group('Group', group_source)
            self.assertEqual(grp.name, 'Group')
            self.assertEqual(grp.source, group_source)
            group_config.add(grp)
            self.assertTrue(grp in group_config)
            self.assertTrue(grp.name in group_config)

    def test_create_group_from_iterable(self):
        with tests.util.temporary_config() as xdg_config:
            grp_a_src = xdg_config.home / 'a'
            grp_a = fool.group.Group('grpa', grp_a_src)
            grp_b_src = xdg_config.home / 'b'
            grp_b = fool.group.Group('grpb', grp_b_src)
            group_config = fool.group.GroupListConfig([grp_a, grp_b])
            self.assertEqual(len(group_config), 2)
            self.assertEqual(group_config['grpa'], grp_a)
            self.assertEqual(group_config['grpb'], grp_b)

    def test_write_one_group_to_file(self):
        with tests.util.temporary_config() as xdg_config:
            group_source = xdg_config.home / 'test'
            grp = fool.group.Group('Group', group_source)
            group_config = fool.group.GroupListConfig([grp])
            group_config.write()
            config_parser = configparser.SafeConfigParser()
            config_parser.read(str(group_config.path))
            group_config.clear_state()
            group_config = fool.group.GroupListConfig()
            self.assertEqual(len(group_config), 0)
            group_config = group_config.from_config_file(config_parser)
            self.assertEqual(group_config['Group'].source, group_source)
            self.assertEqual(group_config['Group'].destination, xdg_config.home)

    def test_walk_group_files(self):
        with tests.util.temporary_config() as xdg_config:
            group_source = xdg_config.home / 'test'
            group_source.mkdir()
            (group_source / 'a').mknod()
            (group_source / 'b').mknod()
            grp = fool.group.Group('main', group_source)
            grp_files = set(grp.files())
            self.assertEqual(grp_files, set({group_source / 'b',
                                             group_source / 'a'}))

    def test_group_object_lists(self):
        with tests.util.temporary_config() as xdg_config:
            group_source = xdg_config.home / 'test'
            group_source.mkdir()
            (group_source / 'a').mknod()
            (group_source / 'b').mknod()
            grp = fool.group.Group('main', group_source)
            grp_objects = set(map(lambda e: e.tuple(),
                                   grp.group_objects()))
            expected = set({(group_source / 'a', xdg_config.home / 'a'),
                            (group_source / 'b', xdg_config.home / 'b')})
            self.assertEqual(expected, grp_objects)

    def test_link_simple_group(self):
        with tests.util.temporary_config() as xdg_config:
            group_source = xdg_config.home / 'test'
            group_source.mkdir()
            (group_source / 'a').mknod()
            (group_source / 'b').mknod()
            grp = fool.group.Group('main', group_source)
            grp_files = set(grp.files())
            self.assertEqual(grp_files, set({group_source / 'b',
                                             group_source / 'a'}))
            grp.sync()
            self.assertTrue((xdg_config.home / 'a').exists())
            self.assertTrue((xdg_config.home / 'b').exists())
            self.assertTrue((xdg_config.home / 'a').islink())
            self.assertTrue((xdg_config.home / 'b').islink())
            self.assertEqual((xdg_config.home / 'a').realpath(),
                             group_source / 'a')
            self.assertEqual((xdg_config.home / 'b').realpath(),
                             group_source / 'b')

    def test_link_wont_overwrite(self):
        with tests.util.temporary_config() as xdg_config:
            group_source = xdg_config.home / 'test'
            group_source.mkdir()
            (group_source / 'a').mknod()
            grp = fool.group.Group('main', group_source)
            grp_files = set(grp.files())
            (xdg_config.home / 'a').mknod()
            with self.assertRaises(OSError):
                grp.sync()

    def test_serialize_group_config(self):
        with tests.util.temporary_config() as xdg_config:
            group_source = xdg_config.home / 'test'
            group_source.mkdir()
            (group_source / 'a').mknod()
            grp = fool.group.Group('main', group_source)
            grp.write()
            config_parser = configparser.SafeConfigParser()
            config_parser.read(str(grp.path))
            other = fool.group.Group.from_config_file(config_parser)
            self.assertEqual(other, grp)
