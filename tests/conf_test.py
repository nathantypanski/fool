"""Tests for fool's configuration subsystem."""

from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals

import os
import os.path
import unittest

import fool.conf
import fool.xdg

import tests.util

class UnitTest(unittest.TestCase):

    def test_config_data_home_ends_with_fool(self):
        conf = fool.conf.ConfigDirectories()
        _, name = conf.data_dir.split()
        self.assertEqual(name, 'fool')

    def test_config_config_home_ends_with_fool(self):
        conf = fool.conf.ConfigDirectories()
        _, name = conf.config_dir.split()
        self.assertEqual(name, 'fool')

    def test_create_config_dir(self):
        with tests.util.temporary_config() as xdg_config:
            tempdir = xdg_config.home
            dirconf = fool.conf.ConfigDirectories()
            self.assertEqual(dirconf.config_dir,
                             tempdir / '.config' / 'fool')
            self.assertFalse(dirconf.config_dir.exists())
            dirconf.create_config_dir()
            self.assertTrue(dirconf.config_dir.isdir())

    def test_create_data_dir(self):
        with tests.util.temporary_config() as xdg_config:
            tempdir = xdg_config.home
            dirconf = fool.conf.ConfigDirectories()
            self.assertEqual(dirconf.data_dir,
                             tempdir / '.local' / 'share' / 'fool')
            self.assertFalse(dirconf.data_dir.exists())
            dirconf.create_data_dir()
            self.assertTrue(dirconf.data_dir.exists())

    def test_config_files_are_relative_to_paths(self):
        conf_file = fool.conf.ConfigFile('world', '/hello')
        self.assertEqual(conf_file.path, '/hello/world')

    def test_config_paths_joined_intelligently(self):
        conf_file = fool.conf.ConfigFile('world', '/hello/')
        self.assertEqual(conf_file.path, '/hello/world')

    def test_can_create_new_configfile_in_existing_directory(self):
        with tests.util.temporary_directory() as tempdir:
            conf_file = fool.conf.ConfigFile('world', tempdir)
            self.assertFalse(conf_file.exists())
            conf_file.write()
            self.assertTrue(conf_file.exists())
            self.assertTrue((fool.files.FoolPath(tempdir) / 'world').exists)
            self.assertTrue((fool.files.FoolPath(tempdir) / 'world').isfile)

    def test_can_create_new_configfile(self):
        with tests.util.temporary_directory() as tempdir:
            conf_file = fool.conf.ConfigFile('a/b', tempdir)
            self.assertFalse(conf_file.exists())
            conf_file.write()
            self.assertTrue(conf_file.exists())
            self.assertTrue((tempdir / 'a' / 'b').exists())
            self.assertTrue((tempdir / 'a' / 'b').isfile())
