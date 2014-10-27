import unittest

import fool.files
import util

class UnitTest(unittest.TestCase):

    def test_walk_files(self):
        with util.temporary_directory() as tempdir:
            (tempdir / 'a').mkdir()
            (tempdir / 'b').mknod()
            (tempdir / 'c').mknod()
            (tempdir / 'a' / 'd').mknod()
            (tempdir / 'a' / 'e').mknod()
            self.assertEqual(list(tempdir.walk_files()),
                             [tempdir / 'c',
                              tempdir / 'b',
                              tempdir / 'a' / 'e',
                              tempdir / 'a' / 'd'])
