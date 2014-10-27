#!/usr/bin/env python

"""A test suite that runs all tests for pyfakefs at once."""

from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals

import unittest

import tests.conf_test
import tests.conflicts_test
import tests.files_test
import tests.group_test
import tests.xdg_test

class AllTests(unittest.TestSuite):
    """A test suite that runs all tests at once."""

    def suite(self):
        loader = unittest.defaultTestLoader
        self.addTests([
            loader.loadTestsFromModule(tests.conf_test),
            loader.loadTestsFromModule(tests.conflicts_test),
            loader.loadTestsFromModule(tests.files_test),
            loader.loadTestsFromModule(tests.group_test),
            loader.loadTestsFromModule(tests.xdg_test),
        ])
        return self

def main():
    result = unittest.TextTestRunner(verbosity=2).run(AllTests().suite())
    if not result.wasSuccessful():
        exit(1)


if __name__ == '__main__':
    main()
