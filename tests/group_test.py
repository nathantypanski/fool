"""fool group test suite"""

import unittest

import fool.group

class UnitTest(unittest.TestCase):

    def test_group_with_name_and_path(self):
        xdg_config = fool.xdg.XDGConfig(xdg=xdg)
        grp = fool.group.Group('Group', '/tmp/group/test')
        self.assertEqual(grp.name('Group'))
        self.assertEqual(grp.source('/tmp/group/test'))
        self.assertEqual(grp.source(xdg.config_home))
