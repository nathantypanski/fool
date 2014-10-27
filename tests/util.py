"""fool test utility code"""

from __future__ import division
from __future__ import unicode_literals

import contextlib
import shutil
import tempfile
import os

from six.moves import map

import fool.xdg
import fool.conf
import fool.group
import fool.files

@contextlib.contextmanager
def temporary_directory(*args, **kwargs):
    d = tempfile.mkdtemp(*args, **kwargs)
    try:
        yield fool.files.FoolPath(d)
    finally:
        shutil.rmtree(d)

@contextlib.contextmanager
def temporary_config(*args, **kwargs):
    """ Create a temporary XDG configuration """
    borg_objects = [fool.xdg.XDGConfig,
                    fool.conf.ConfigDirectories,
                    fool.group.GroupConfig]
    try:
        for obj in borg_objects:
            obj.clear_state()
        with temporary_directory() as tempdir:
            xdg = fool.xdg.XDGConfig()
            xdg.home = tempdir
            assert not xdg.home.startswith(os.environ['HOME'])
            assert not xdg.config_home.startswith(os.environ['HOME'])
            assert not xdg.data_home.startswith(os.environ['HOME'])
            yield xdg
    finally:
        for obj in borg_objects:
            obj.clear_state()
