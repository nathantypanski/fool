
from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals

import unittest

import fool.files
import tests.util

class UnitTest(unittest.TestCase):

    def test_walk_files(self):
        with tests.util.temporary_directory() as tempdir:
            (tempdir / 'a').mkdir()
            (tempdir / 'b').mknod()
            (tempdir / 'c').mknod()
            (tempdir / 'a' / 'd').mknod()
            (tempdir / 'a' / 'e').mknod()
            self.assertEqual(set(tempdir.walk_files()),
                             set({tempdir / 'c',
                                  tempdir / 'b',
                                  tempdir / 'a' / 'e',
                                  tempdir / 'a' / 'd'}))
