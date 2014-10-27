
from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals

import unittest

import fool.files

class UnitTest(unittest.TestCase):

    def test_walk_files(self):
        with fool.files.temporary_directory() as tempdir:
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

    def test_foolfile_symlink(self):
        with fool.files.temporary_directory() as tempdir:
            a = (tempdir / 'src' / 'a')
            fool.files.create_subdirs(a)
            a.mknod()
            b = tempdir / 'b'
            a.symlink(b)
            self.assertTrue(b.islink())
            self.assertEqual(a, b.realpath())

    def test_foolfile_symlink_existing_raises_oserror(self):
        with fool.files.temporary_directory() as tempdir:
            a = tempdir / 'a'
            b = tempdir / 'b'
            a.mknod()
            b.mknod()
            with self.assertRaises(OSError):
                a.symlink(b)
