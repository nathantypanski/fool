
from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals

import unittest

import fool.chapter
import tests.util

class UnitTest(unittest.TestCase):

    def test_pure_chapter_with_name(self):
        chapter = fool.chapter.PureChapter('Test')
        self.assertEqual(chapter.name, 'Test')

    def test_pure_chapter_rename(self):
        chapter = fool.chapter.PureChapter('Test')
        self.assertEqual(chapter.name, 'Test')
        chapter.rename('Rest')
        self.assertEqual(chapter.name, 'Rest')

    def test_chapter_creates_directory(self):
        with tests.util.temporary_config() as xdg_config:
            conf = fool.conf.ConfigDirectories()
            path = (conf.chapter_dir / 'Test').normpath().abspath()
            self.assertFalse(path.exists())
            self.assertFalse(path.isdir())
            chapter = fool.chapter.Chapter('Test')
            self.assertEqual(chapter.dirpath, path)
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
            import os
            print(os.listdir(str(path.dirname())))
            self.assertFalse(path.exists())
            self.assertFalse(path.isdir())
            self.assertTrue(renamed_path.exists())
            self.assertTrue(renamed_path.isdir())
