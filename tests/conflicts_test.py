
import unittest

import fool.conflicts
import fool.files

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
