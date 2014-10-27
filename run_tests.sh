#!/usr/bin/env sh

set -e

/usr/bin/env python2 tests/run_tests.py
/usr/bin/env python3 tests/run_tests.py
