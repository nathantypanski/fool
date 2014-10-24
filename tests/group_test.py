"""fool group test suite"""

import unittest

import fool.group

class UnitTest(unittest.TestCase):

    def test_group_with_name_and_path(self):
        grp = fool.group.Group('Group', '/tmp/group/test')
        self.assertEqual(grp.name('Group'))
        self.assertEqual(grp.path('/tmp/group/test'))
