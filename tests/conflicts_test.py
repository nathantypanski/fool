
import unittest

import fool.conflicts
import fool.files
import tests.util

class UnitTest(unittest.TestCase):

    def test_foolfile_overwrite_existing_location(self):
        with fool.files.temporary_directory() as tempdir:
            a = tempdir / 'a'
            b = tempdir / 'b'
            a.mknod()
            b.mknod()
            with self.assertRaises(OSError):
                a.symlink(b)
            resolver = fool.conflicts.OverwriteResolver(a, b)
            resolver.resolve()
            self.assertTrue(b.islink())
            self.assertEqual(a, b.realpath())

    def test_group_overwrite_with_overwrite_resolver(self):
        with tests.util.temporary_config() as xdg_config:
            group_source = xdg_config.home / 'test'
            group_source.mkdir()
            src = group_source / 'a'
            src.mknod()
            grp = fool.group.Group('main', group_source)
            dest = xdg_config.home / 'a'
            dest.mknod()
            self.assertTrue(src.exists())
            self.assertTrue(dest.exists())
            grp.sync(resolver=fool.conflicts.OverwriteResolver)
            self.assertEqual(src, dest.realpath())
            self.assertTrue(dest.islink())
