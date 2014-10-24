"""XDG Base Directory Specification config tests for fool"""

import unittest
import fool.xdg

class TestCase(unittest.TestCase):

    def test_get_xdg_home(self):
        xdg = fool.xdg.XDG()
        self.assertIsInstance(xdg.home, str)

    def test_get_xdg_data_home(self):
        xdg = fool.xdg.XDG()
        self.assertIsInstance(xdg.data_home, str)

    def test_get_xdg_config_home(self):
        xdg = fool.xdg.XDG()
        self.assertIsInstance(xdg.config_home, str)

    def test_config_data_home_ends_with_fool(self):
        conf = fool.xdg.XDGConfig()
        self.assertTrue(conf.data_dir.endswith('fool'))

    def test_config_config_home_ends_with_fool(self):
        conf = fool.xdg.XDGConfig()
        self.assertTrue(conf.config_dir.endswith('fool'))
