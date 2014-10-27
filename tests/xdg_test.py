"""XDG Base Directory Specification config tests for fool"""

import unittest

import fool.files
import fool.xdg

class TestCase(unittest.TestCase):

    def test_get_xdg_home(self):
        xdg = fool.xdg.XDGConfig()
        self.assertIsInstance(xdg.home, fool.files.Path)

    def test_get_xdg_data_home(self):
        xdg = fool.xdg.XDGConfig()
        self.assertIsInstance(xdg.data_home, fool.files.Path)

    def test_get_xdg_config_home(self):
        xdg = fool.xdg.XDGConfig()
        self.assertIsInstance(xdg.config_home, fool.files.Path)

