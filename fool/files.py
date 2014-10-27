
from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals

import contextlib
import errno
import os
import os.path
import shutil

import six

import tempfile


class FoolPath(object):
    """Wrapper around os.path for ease of use."""

    def __init__(self, pathname):
        if isinstance(pathname, FoolPath):
            pathname = pathname.pathname
        self._pathname = pathname

    @property
    def pathname(self):
        """Immutable string representation of this pathname."""
        return self._pathname

    def abspath(self):
        """Absolute path."""
        return FoolPath(os.path.abspath(self.pathname))

    def basename(self):
        """The final component of this pathname."""
        return FoolPath(os.path.basename(self.pathname))

    def dirname(self):
        """The directory component of this pathname."""
        return FoolPath(os.path.dirname(self.pathname))

    def exists(self):
        """Test whether this path exists.

        This is False for broken symbolic links.
        """
        return os.path.exists(self.pathname)

    def lexists(self):
        """Test whether this path exists.

        This is True for broken symbolic links.
        """
        return os.path.lexists(self.pathname)

    def expanduser(self):
        """Expand ~ and ~user constructions.

        If user or $HOME is unknown, do nothing.
        """
        return FoolPath(os.path.expanduser(self.pathname))

    def expandvars(self):
        """Expand shell variables of form $var and ${var}.

        Unknown variables are left unchanged.
        """
        return FoolPath(os.path.expandvars(self.pathname))

    def atime(self):
        """The last access time of this file, reported by os.stat()."""
        return os.path.getatime(self.pathname)

    def mtime(self):
        """The last modification time of this file, reported by os.stat()."""
        return os.path.getmtime(self.pathname)

    def ctime(self):
        """The metadata change time of this file, reported by os.stat()."""
        return os.path.getctime(self.pathname)

    def size(self):
        """The size of this file, reported by os.stat()."""
        return os.path.getsize(self.pathname)

    def isabs(self):
        """Test whether this path is absolute."""
        return os.path.isabs(self.pathname)

    def isfile(self):
        """Test whether this path is a file."""
        return os.path.isfile(self.pathname)

    def isdir(self):
        """Test whether this path is a directory."""
        return os.path.isdir(self.pathname)

    def islink(self):
        """Test whether this path is a symbolic link."""
        return os.path.islink(self.pathname)

    def ismount(self):
        """Test whether this path is a mount point."""
        return os.path.ismount(self.pathname)

    def join(self, *paths):
        return FoolPath(os.path.join(self.pathname, *paths))

    def normpath(self):
        """Normalize a path, eliminating double slashes, etc."""
        return FoolPath(os.path.normpath(self.pathname))

    def relpath(self, start=None):
        """Return a relative path either from the current directory or start.

        Keyword args:
            start: Optional start directory. Defaults to os.curdir.
        """
        if start is None:
            start = os.curdir
        return FoolPath(os.path.relpath(self.pathname, six.text_type(start)))

    def realpath(self):
        """Follow symlinks to the canonical location of this path."""
        return FoolPath(os.path.realpath(self.pathname))

    def open(self, *args, **kwargs):
        """Open this path, passing all arguments to open()."""
        return open(self.pathname, *args, **kwargs)

    def samefile(self, other):
        """Test whether this path and other reference the same actual file."""
        return os.path.samefile(self.pathname, other)

    def split(self):
        head, tail = os.path.split(self.pathname)
        return FoolPath(head), FoolPath(tail)

    def splitext(self):
        head, tail = os.path.splitext(self.pathname)
        return head, tail

    def splitunc(self):
        head, tail = os.path.splitunc(self.pathname)
        return FoolPath(head), FoolPath(tail)

    def walk(self, topdown=True, onerror=None, followlinks=False):
        """Same as os.walk on this path."""
        return os.walk(self.pathname, topdown, onerror, followlinks)

    def walk_files(self, topdown=True, onerror=None, followlinks=False):
        """Walk the reachable files from this path.

        Yields:
            Path objects for each file reachable from this path.
        """
        for root, dirs, files in os.walk(self.pathname, topdown, onerror, followlinks):
            for name in files:
                yield FoolPath(root) / name

    def mkdir(self, mode=0o777):
        """Create a directory at this path."""
        return os.mkdir(self.pathname, mode)

    def mknod(self, mode=0o0600, device=0):
        """Create a directory at this path."""
        return os.mknod(self.pathname, mode, device)

    def symlink(self, link_name):
        """Create a symbolic link pointing to this path named link_name."""
        return os.symlink(six.text_type(self.pathname), six.text_type(link_name))

    def rename(self, dest_name):
        """Rename this file to dest_name."""
        return os.rename(self.pathname, six.text_type(dest_name))

    def startswith(self, value):
        return self.pathname.startswith(value)

    def endswith(self, value):
        return self.pathname.endswith(value)

    def rfind(self, value):
        return self.pathname.rfind(value)

    def __getitem__(self, value):
        return self.pathname[value]

    def __str__(self):
        return self.pathname

    def __repr__(self):
        return 'FoolPath("{}")'.format(self.pathname)

    def __hash__(self):
        return hash(self.pathname)

    def __add__(self, other):
        return self / other

    def __eq__(self, other):
        if isinstance(other, six.string_types):
            return self.pathname == other
        else:
            try:
                return self.pathname == other.pathname
            except AttributeError:
                return False

    def __div__(self, other):
        if isinstance(other, FoolPath):
            return FoolPath(os.path.join(self.pathname, other.pathname))
        else:
            return FoolPath(os.path.join(self.pathname, other))

    def __truediv__(self, other):
        return self.__div__(other)


@contextlib.contextmanager
def temporary_directory(*args, **kwargs):
    """Create a temporary directory with the supplied arguments.

    Yields:
        A temporary directory that will be removed upon context exit.
    """
    d = tempfile.mkdtemp(*args, **kwargs)
    try:
        yield FoolPath(d)
    finally:
        shutil.rmtree(d)


@contextlib.contextmanager
def temporary_directory_chdir(*args, **kwargs):
    """Create a temporary directory with the supplied arguments.

    Changes directories into the temporary directory while within the context.

    Yields:
        A temporary directory that will be removed upon context exit.
    """
    old_cwd = os.getcwd()
    d = tempfile.mkdtemp(*args, **kwargs)
    try:
        os.chdir(d)
        yield FoolPath(d)
    finally:
        os.chdir(old_cwd)
        shutil.rmtree(d)


def create_subdirs(path):
    """Create necessary subdirectories leading up to path.

    Args:
        path: path to which directories will be created. Note that path
            itself will not be created.
    """
    try:
        os.makedirs(six.text_type(FoolPath(path).dirname()))
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise exception
        else:
            pass

