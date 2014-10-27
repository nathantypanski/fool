#!/usr/bin/env python

"""A test suite that runs all tests for pyfakefs at once."""

from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals

import unittest

import tests.xdg_test
import tests.conf_test
import tests.group_test
import tests.files_test

class AllTests(unittest.TestSuite):
    """A test suite that runs all tests at once."""

    def suite(self):
        loader = unittest.defaultTestLoader
        self.addTests([
            loader.loadTestsFromModule(tests.xdg_test),
            loader.loadTestsFromModule(tests.conf_test),
            loader.loadTestsFromModule(tests.group_test),
            loader.loadTestsFromModule(tests.files_test),
        ])
        return self

def main():
    unittest.TextTestRunner(verbosity=2).run(AllTests().suite())

if __name__ == '__main__':
    main()
