
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
            path = (conf / 'Test').normpath().abspath()
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
