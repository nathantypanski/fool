"""fool test utility code"""

import contextlib
import shutil
import tempfile

import fool.xdg

@contextlib.contextmanager
def temporary_directory(*args, **kwargs):
    d = tempfile.mkdtemp(*args, **kwargs)
    try:
        yield d
    finally:
        shutil.rmtree(d)

@contextlib.contextmanager
def temporary_config(*args, **kwargs):
    try:
        with temporary_directory() as tempdir:
            xdg = fool.xdg.XDGConfig()
            xdg.home = tempdir
            yield xdg
    finally:
        fool.xdg.XDGConfig.clear_state()
