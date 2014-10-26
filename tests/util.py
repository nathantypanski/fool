"""fool test utility code"""

import contextlib
import shutil
import tempfile
import os

import fool.xdg
import fool.conf
import fool.group

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
    borg_objects = [fool.xdg.XDGConfig,
                    fool.conf.ConfigDirectories,
                    fool.group.GroupConfig]
    clear_state = lambda o: o.clear_state()
    try:
        map(clear_state, borg_objects)
        with temporary_directory() as tempdir:
            xdg = fool.xdg.XDGConfig()
            xdg.home = tempdir
            assert not xdg.home.startswith(os.environ['HOME'])
            assert not xdg.config_home.startswith(os.environ['HOME'])
            assert not xdg.data_home.startswith(os.environ['HOME'])
            yield xdg
    finally:
        map(clear_state, borg_objects)
