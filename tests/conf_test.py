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
