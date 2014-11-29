
from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals

import sys

import six

import fool.files

class DirectoryObject(object):
    """An object that is tied by name to a directory.

    Args:
        name: the name of this object
        dirpath_func: a function that calculates a directory path,
            given a name. Defaults to the name.
    """

    def __init__(self, name, dirpath_func=None):
        self._name = name
        if dirpath_func is None:
            dirpath_func = lambda x: x
        self._dirpath_func = dirpath_func
        self._make_exist()

    @property
    def name(self):
        """Name of this DirectoryObject."""
        return self._name

    @property
    def dirpath(self):
        """Path to the directory assocated with this DirectoryObject."""
        return self._dirpath_func(self.name)

    def contents(self):
        return self.dirpath.walk_files()

    def _make_exist(self):
        if not self.dirpath.exists():
            fool.files.create_subdirs(self.dirpath)
            self.dirpath.mkdir()

    def rename(self, newname):
        """Rename this DirectoryObject."""
        self.dirpath.rename(self._dirpath_func(newname))
        self._name = newname


class GroupObject(object):
    """An object for syncing with fool.

    A GroupObject is pathname and a destination link pathname, representing
    the source pathname and the destination pathname of a desired link.

    Args:
        source: source pathname for this GroupObject.
        destination: destination pathname for this GroupObject.
    """

    def __init__(self, source, destination):
        self.source = fool.files.FoolPath(source)
        self.destination = fool.files.FoolPath(destination)

    @property
    def synced(self):
        """Test whether the destination is a symlink to the source."""
        return (self.destination.islink()
                and self.source == self.destination.realpath())

    def sync(self, resolver=None):
        """Create a symbolic link from the source to destination.

        Do nothing if already synced.

        Keyword args:
            resolver: Resolver class used to handle flile conflicts.
        """
        if self.synced:
            return
        if resolver is not None and not hasattr(resolver, 'resolve'):
            raise TypeError('resolver must have a resolve() method')
        try:
            self.source.symlink(self.destination)
        except OSError as exception:
            if resolver is not None:
                resolver(self.source, self.destination, exception).resolve()
            else:
                six.reraise(*sys.exc_info())

    def tuple(self):
        """Return a tuple of source, destination."""
        return self.source, self.destination

    def __repr__(self):
        return "GroupObject({}, {})".format(self.source, self.destination)

