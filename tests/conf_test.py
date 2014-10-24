"""Tests for fool's configuration subsystem."""

import contextlib
import os
import shutil
import tempfile
import unittest

import fool.conf
import fool.xdg

@contextlib.contextmanager
def temporary_directory(*args, **kwargs):
    d = tempfile.mkdtemp(*args, **kwargs)
    try:
        yield d
    finally:
        shutil.rmtree(d)

class UnitTest(unittest.TestCase):

    def setUp(self):
        fool.conf.ConfigDirectories.clear_state()

    def test_create_config_dir(self):
        with temporary_directory() as tempdir:
            xdg = fool.xdg.XDG()
            xdg.config_home = tempdir
            xdg_config = fool.xdg.XDGConfig(xdg=xdg)
            dirconf = fool.conf.ConfigDirectories(xdg_config=xdg_config)
            self.assertEqual(dirconf.config_dir, tempdir + '/fool')
            self.assertFalse(os.path.exists(dirconf.config_dir))
            dirconf.create_config_dir()
            self.assertTrue(os.path.isdir(dirconf.config_dir))

    def test_create_data_dir(self):
        with temporary_directory() as tempdir:
            xdg = fool.xdg.XDG()
            xdg.data_home = tempdir
            xdg_config = fool.xdg.XDGConfig(xdg=xdg)
            dirconf = fool.conf.ConfigDirectories(xdg_config=xdg_config)
            self.assertEqual(dirconf.data_dir, tempdir + '/fool')
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
        with temporary_directory() as tempdir:
            conf_file = fool.conf.ConfigFile('world', tempdir)
            self.assertFalse(conf_file.exists)
            conf_file.create()
            self.assertTrue(conf_file.exists)
            self.assertTrue(os.path.exists(os.path.join(tempdir, 'world')))
            self.assertTrue(os.path.isfile(os.path.join(tempdir, 'world')))

    def test_can_create_new_configfile(self):
        with temporary_directory() as tempdir:
            conf_file = fool.conf.ConfigFile('a/b', tempdir)
            self.assertFalse(conf_file.exists)
            conf_file.create()
            self.assertTrue(conf_file.exists)
            self.assertTrue(os.path.exists(os.path.join(tempdir, 'a', 'b')))
            self.assertTrue(os.path.isfile(os.path.join(tempdir, 'a', 'b')))
