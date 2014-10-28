
from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals

import unittest

import fool.section
import tests.util

class UnitTest(unittest.TestCase):

    def test_section(self):
        with tests.util.temporary_config() as xdg_config:
            conf = fool.conf.ConfigDirectories()
            path = (conf.section_dir / 'Test').normpath().abspath()
            self.assertFalse(path.exists())
            self.assertFalse(path.isdir())
            section = fool.section.Section('Test')
            self.assertEqual(section.dirpath, path)
            self.assertTrue(path.exists())
            self.assertTrue(path.isdir())

    def test_create_two_chapters_with_same_name(self):
        with tests.util.temporary_config() as xdg_config:
            chapter_a = fool.chapter.Chapter('Test')
            chapter_b = fool.chapter.Chapter('Test')

    def test_rename_a_chapter(self):
        with tests.util.temporary_config() as xdg_config:
            conf = fool.conf.ConfigDirectories()
            path = (conf.chapter_dir / 'Test').normpath().abspath()
            renamed_path = (conf.chapter_dir / 'Rest').normpath().abspath()
            self.assertFalse(path.exists())
            self.assertFalse(path.isdir())
            self.assertFalse(renamed_path.exists())
            self.assertFalse(renamed_path.isdir())
            chapter = fool.chapter.Chapter('Test')
            self.assertTrue(path.exists())
            self.assertTrue(path.isdir())
            chapter.rename('Rest')
            self.assertFalse(path.exists())
            self.assertFalse(path.isdir())
            self.assertTrue(renamed_path.exists())
            self.assertTrue(renamed_path.isdir())
