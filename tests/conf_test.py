"""Tests for fool's configuration subsystem."""

import os
import os.path
import unittest

import fool.conf
import fool.xdg

import util

class UnitTest(unittest.TestCase):

    def test_config_data_home_ends_with_fool(self):
        conf = fool.conf.ConfigDirectories()
        _, name = os.path.split(conf.data_dir)
        self.assertEqual(name, 'fool')

    def test_config_config_home_ends_with_fool(self):
        conf = fool.conf.ConfigDirectories()
        _, name = os.path.split(conf.config_dir)
        self.assertEqual(name, 'fool')

    def test_create_config_dir(self):
        with util.temporary_config() as xdg_config:
            tempdir = xdg_config.home
            dirconf = fool.conf.ConfigDirectories()
            self.assertEqual(dirconf.config_dir,
                             os.path.join(tempdir, '.config', 'fool'))
            self.assertFalse(os.path.exists(dirconf.config_dir))
            dirconf.create_config_dir()
            self.assertTrue(os.path.isdir(dirconf.config_dir))

    def test_create_data_dir(self):
        with util.temporary_config() as xdg_config:
            tempdir = xdg_config.home
            dirconf = fool.conf.ConfigDirectories()
            self.assertEqual(dirconf.data_dir,
                             os.path.join(tempdir, '.local', 'share', 'fool'))
            self.assertFalse(os.path.exists(dirconf.data_dir))
            dirconf.create_data_dir()
            self.assertTrue(os.path.isdir(dirconf.data_dir))

    def test_config_files_are_relative_to_paths(self):
        conf_file = fool.conf.ConfigFile('world', '/hello')
        self.assertEqual(conf_file.path, '/hello/world')

    def test_config_paths_joined_intelligently(self):
        conf_file = fool.conf.ConfigFile('world', '/hello/')
        self.assertEqual(conf_file.path, '/hello/world')

    def test_can_create_new_configfile_in_existing_directory(self):
        with util.temporary_directory() as tempdir:
            conf_file = fool.conf.ConfigFile('world', tempdir)
            self.assertFalse(conf_file.exists)
            conf_file.create()
            self.assertTrue(conf_file.exists)
            self.assertTrue(os.path.exists(os.path.join(tempdir, 'world')))
            self.assertTrue(os.path.isfile(os.path.join(tempdir, 'world')))

    def test_can_create_new_configfile(self):
        with util.temporary_directory() as tempdir:
            conf_file = fool.conf.ConfigFile('a/b', tempdir)
            self.assertFalse(conf_file.exists)
            conf_file.create()
            self.assertTrue(conf_file.exists)
            self.assertTrue(os.path.exists(os.path.join(tempdir, 'a', 'b')))
            self.assertTrue(os.path.isfile(os.path.join(tempdir, 'a', 'b')))
