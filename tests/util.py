"""fool test utility code"""

import contextlib
import shutil
import tempfile
import os

import fool.xdg
import fool.conf

@contextlib.contextmanager
def temporary_directory(*args, **kwargs):
    d = tempfile.mkdtemp(*args, **kwargs)
    try:
        yield d
    finally:
        shutil.rmtree(d)

@contextlib.contextmanager
def temporary_config(*args, **kwargs):
    """ Create a temporary XDG configuration """
    try:
        fool.xdg.XDGConfig.clear_state()
        fool.conf.ConfigDirectories.clear_state()
        with temporary_directory() as tempdir:
            xdg = fool.xdg.XDGConfig()
            xdg.home = tempdir
            assert not xdg.home.startswith(os.environ['HOME'])
            assert not xdg.config_home.startswith(os.environ['HOME'])
            assert not xdg.data_home.startswith(os.environ['HOME'])
            yield xdg
    finally:
        fool.xdg.XDGConfig.clear_state()
        fool.conf.ConfigDirectories.clear_state()
