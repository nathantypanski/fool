
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
            srcdir = xdg_config.home / 'src'
            a =  srcdir / 'a'
            srcdir.mkdir()
            with a.open('w') as textfile:
                textfile.write('hello')
