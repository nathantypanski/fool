#!/usr/bin/env python

import setuptools

setuptools.setup(
    name = "fool",
    version = "0.1",
    scripts = ['fool.py'],
    packages = setuptools.find_packages(),
    install_requires = ['six'],
)
