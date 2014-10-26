"""fool group test suite"""

import unittest
import os

import fool.group
import util

class UnitTest(unittest.TestCase):

    def test_group_with_name_and_path(self):
        with util.temporary_config() as xdg_config:
            group_config = fool.conf.GroupConfig()
            group_source = os.path.join(xdg_config.home, 'test')
            grp = fool.group.Group('Group', group_source)
            self.assertEqual(grp.name, 'Group')
            self.assertEqual(grp.source, group_source)
            self.assertTrue(grp in group_config)
