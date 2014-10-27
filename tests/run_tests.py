#!/usr/bin/env python2

"""A test suite that runs all tests for pyfakefs at once."""

from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals

import unittest

import xdg_test
import conf_test
import group_test
import files_test

class AllTests(unittest.TestSuite):
    """A test suite that runs all tests at once."""

    def suite(self):
        loader = unittest.defaultTestLoader
        self.addTests([
            loader.loadTestsFromModule(xdg_test),
            loader.loadTestsFromModule(conf_test),
            loader.loadTestsFromModule(group_test),
            loader.loadTestsFromModule(files_test),
        ])
        return self

def main():
    unittest.TextTestRunner(verbosity=2).run(AllTests().suite())

if __name__ == '__main__':
    main()
